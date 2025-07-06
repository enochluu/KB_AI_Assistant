https://knowledgebase.emergingit.com.au/books/backup-errors-and-fixes/page/failed-to-process-method-there-is-not-enough-space-on-the-disk
# Failed to process method. There is not enough space on the disk.

## **Issue**

You may encounter the following error during a Veeam backup or replication job:

```
Failed to process method. There is not enough space on the disk.
```

This error indicates that the target storage location has insufficient free space to complete the backup or restore operation.

---

## **Cause**

This issue is typically caused by:

- Retention policies retaining too many restore points.
- Backup storage volumes running out of disk space.

---

## **Resolution**

### **Option 1: Reduce Retention Period (TALK WITH CLIENT FIRST)**

1. Get a holistic understanding of the backup retention period, please refer to the section "Things to look out for with Veeam retention period" below. There may not be just incremental backups but also occasional full backups
2. Consult with the client to **shorten the retention policy**. This will reduce the number of restore points stored and free up space over time.

#### Things to look out for with Veeam retention period  


1. Go to **Backup &gt; Right click on the backup job &gt; Edit**

[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/5ycAR3N6RsGYLVIE-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/5ycAR3N6RsGYLVIE-image.png)

##### How to change the retention period  


1. From the previous step, go to **Storage**

[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/ag5wanfAnbcIDX6b-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/ag5wanfAnbcIDX6b-image.png)


#####   
Verify whether the client has full backups implemented in their backup schedule

1. From the previous step go to **Storage &gt; Advanced**

[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/dj6e8KzPyWuN6lgM-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/dj6e8KzPyWuN6lgM-image.png)

##### Verify if the "Defragment and compact full backup file" option is selected

1. From the previous step go to **Storage &gt; Advanced &gt; Maintenance**
2. This option should be unticked, for further details please click [this link](https://helpcenter.veeam.com/docs/backup/vsphere/backup_copy_compact_file.html?ver=120)

### [![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/3DxAC9sXr3WK4L1e-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/3DxAC9sXr3WK4L1e-image.png)  
  
**Option 2: Increase Disk Space (TALK WITH A SENIOR FIRST, THEN CONSULT WITH THE CLIENT)**

- Expand the storage volume where backups are being written.
- Alternatively, move the backup repository to a larger disk or storage location.

### **Option 3: Delete Recovery Points (TALK WITH A SENIOR FIRST)**

- Manually delete older recovery points **only if absolutely necessary**.
- Be extremely careful when deleting **incremental backups**, as this can **break the backup chain** and render restore points unusable. If you break the backup chain all proceeding backups will be orphaned and be unable to be used.