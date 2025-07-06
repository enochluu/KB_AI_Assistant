https://knowledgebase.emergingit.com.au/books/backup-errors-and-fixes/page/the-transfer-of-one-or-more-volume-images-from-a-protected-machine-to-the-core-has-failed
# The transfer of one or more volume images from a protected machine to the Core has failed

### **Issue**

Backup operation fails with the following error:

```
The transfer of one or more volume images from a protected machine to the Core has failed.
The agent dropped the network connection during the data transfer. Check the agent log for possible errors.
The transfer failed for volume 'C:\'
One or more errors occurred.
```

### **Cause**

This issue typically occurs when the **Volume Shadow Copy (VSS) storage** on the protected machine has run out of space. When shadow storage is exhausted, the snapshot required for backup cannot be maintained, causing the agent to drop the connection during data transfer.  
  
To verify this issue:

1. **Check the Event Viewer on the Protected Machine:**
    
    
    - Open **Event Viewer** (`eventvwr.msc`)
    - Navigate to: `Windows Logs > Application`
    - Look for **VSS** or **VolSnap** errors around the time of the backup failure.
    - Common error messages include: 
        - *"The shadow copy storage association could not be made..."*
        - *"Insufficient storage available to create either the shadow copy storage file or other shadow copy data."* [![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/b1bZwR12TQmuSi9p-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/b1bZwR12TQmuSi9p-image.png)
2. **Verify Shadow Storage Usage**:
    
    
    - Open **Command Prompt** as Administrator.
    - Run the following command to check current shadow storage allocation: ```
        vssadmin list shadowstorage
        ```
    - Review the output to determine if the **Maximum Shadow Copy Storage space** is low or insufficient.

### **Resolution**

To confirm and resolve the issue:

1. **Delete Older Shadow Copies via Windows Explorer**: 
    - Open **File Explorer** and right-click on the **C: drive** (or the affected volume).
    - Select **Properties**.
    - Go to the **Shadow Copies** tab (if available).
    - In the list of available shadow copies, select the **oldest entries**.
    - Click **Delete Now** to remove them and free up space.
    - Confirm the deletion when prompted.
2. **Increase Shadow Storage (Optional)**:
    
    
    - If space allows, increase the shadow storage allocation: ```
        vssadmin resize shadowstorage /for=C: /on=C: /maxsize=20%
        ```
        
        > Adjust the `20%` value based on available disk space and backup requirements. (This can also be changed to a specific size e.g. 15GB)
3. **Retry the Backup Job**:
    
    
    - Once space is cleared or resized, reinitiate the backup from the Rapid Recovery Core console.

### **Verification**

- Monitor the backup job to ensure it completes successfully.
- Check the agent logs and Event Viewer to confirm no further VSS-related errors occur.