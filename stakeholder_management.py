import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')

def get_manager_chain(email, target_email=None, max_depth=15):
    """
    Trace the management chain for a given email address.

    Args:
        email: The email address to start from
        target_email: Optional email to check if they report up to (case-insensitive)
        max_depth: Maximum number of levels to traverse
    """
    recipient = namespace.CreateRecipient(email)
    recipient.Resolve()
    if not recipient.Resolved:
        print(f'Could not resolve: {email}')
        return
    user = recipient.AddressEntry.GetExchangeUser()
    if not user:
        print(f'Could not get Exchange user for: {email}')
        return

    print(f'Starting from: {user.Name} ({user.PrimarySmtpAddress})')
    print(f'  Title: {user.JobTitle}')
    print()

    current = user
    for i in range(max_depth):
        manager = current.GetExchangeUserManager()
        if not manager:
            print(f'  [No further manager found]')
            break
        print(f'Level {i+1}: {manager.Name} ({manager.PrimarySmtpAddress})')
        print(f'  Title: {manager.JobTitle}')
        if target_email and manager.PrimarySmtpAddress.lower() == target_email.lower():
            print(f'\n*** YES - reports up to {target_email} at level {i+1} ***')
            return True
        current = manager

    if target_email:
        print(f'\nDid not find {target_email} in the management chain.')
        return False


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python stakeholder_management.py <email> [target_email]')
        print('  email: The email address to look up')
        print('  target_email: Optional - check if they report up to this person')
        print()
        print('Examples:')
        print('  python stakeholder_management.py GargK@aetna.com')
        print('  python stakeholder_management.py GargK@aetna.com BurnettC@cvshealth.com')
    else:
        email = sys.argv[1]
        target = sys.argv[2] if len(sys.argv) > 2 else None
        get_manager_chain(email, target_email=target)
