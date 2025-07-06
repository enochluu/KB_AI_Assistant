https://knowledgebase.emergingit.com.au/books/backup-errors-and-fixes/page/failed-to-prepare-guest-for-hot-backup-details-failed-to-connect-to-guest-agent-errors-cannot-connect-to-the-admin-share
# Failed to prepare guest for hot backup. Details: Failed to connect to guest agent.  Errors: 'Cannot connect to the admin share.

### **Issue**

Backup operation fails with the following error:

```
Failed to prepare guest for hot backup. Details: Failed to connect to guest agent. 
Errors: 'Cannot connect to the admin share. 
Host: [SERVER_NAME.CLIENT_NAME.com]. Account: [CLIENT_NAME\administrator]. 
Win32 error: The referenced account is currently locked out and may not be logged on to. Code: 1909

```

### **Cause**

The backup process attempts to connect to the guest VM using the specified domain account (`CLIENT_NAME\administrator`). However, the account is **locked out**, preventing access to the admin share and guest agent.

### **Resolution**

To resolve this issue:

1. **Log into Active Directory** using an account with administrative privileges.
2. Open **Active Directory Users and Computers (ADUC)**.
3. Navigate to the **Users** container or the appropriate **OU** where the `CLIENT_NAME\administrator` account resides.
4. Locate and **right-click** the `administrator` account.
5. Select **Properties** &gt; **Account** tab.
6. If the account is locked, you will see a checkbox labeled **"Unlock account"**.
7. Check the box and click **OK** to unlock the account.
8. On the VBR server performing the Veeam backup, click on the Hamburger menu then **Credentials &amp; Passwords &gt; Datacenter Credentials**[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/ZDJpLeJe7IK0RRq6-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/ZDJpLeJe7IK0RRq6-image.png)
9. Select the credential that was previously locked and update the credential following the prompts. Save the changes.

### **Verification**

After unlocking the account and updating credentials on Veeam:

- Retry the backup operation.
- Confirm that the guest agent can now be contacted and the backup proceeds without errors.