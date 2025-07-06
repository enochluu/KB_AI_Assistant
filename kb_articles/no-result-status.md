https://knowledgebase.emergingit.com.au/books/backup-errors-and-fixes/page/no-result-status
# No Result Status

## **Issue**

You may encounter a **"No Result"** status in Backup Radar for one or more backup jobs. This status indicates that Backup Radar has not received any backup report data for the expected time window.

---

## **Cause**

This issue can be caused by several factors, including:

- The backup job did not run or failed silently.
- The backup report email was not sent or received.
- The backup job is taking longer than expected (e.g., **12+ hours**), causing the report to be sent **after** Backup Radar’s status check time.
- The **Backup Radar job is not configured to check at the correct time**.
- The **backup job name has changed** or the **server was migrated**, resulting in a new job being created in Backup Radar that needs to be manually merged.

---

## **Resolution**

### **1. Verify Backup Job Execution**

- Log into the **server performing the backup** (e.g., Quest, Veeam, etc.).
- Confirm that the backup job **ran successfully** and completed within the expected time frame.
- Check the local backup logs for any errors or skipped jobs.

### **2. Check for Long-Running Jobs**

- Determine whether the backup job is taking an unusually long time to complete (e.g., **12+ hours**).
- If the job finishes **after** the Backup Radar status check time, it may not be picked up in time.
- Consider adjusting the backup schedule or the status check time accordingly.

### **3. Check Email Delivery**

- Ensure that the backup software successfully **sent the report email**.
- Verify that the email was **delivered to Backup Radar** by checking our filtering service, **MailGuard**.
- Look for any SMTP errors or delivery failures in the backup software’s logs.

### **4. Confirm Backup Radar Job Timing**

- In the **Backup Radar portal**, open the affected job.
- Ensure the **“Status Calculation Time”** is set appropriately—typically **12:00 AM** for daily jobs.
- Adjust the time if the backup job runs later or earlier than expected.

### **5. Check for Job Name Changes or Server Migrations**

- If the **backup job name has changed** or the **server was migrated**, Backup Radar may treat it as a **new job**.
- In this case, you will need to **activate and manually merge the new job** with the existing one in Backup Radar to maintain continuity and reporting accuracy.
- Before proceeding with the following steps, ensure you are activating the correct backup by ensuring the **Job Name** matches what is on the platform performing the backup as well as the **Backup Method**
    1. Click on **Manage &gt; Activate Backups &gt;** Input the **Device Name** &gt; **Select the checkbox for the desired backup** &gt; **Bulk Activate**[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/zZWTsmnOrW6GaT6b-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/zZWTsmnOrW6GaT6b-image.png)
    2. After this, head to **Audit &gt; Select the checkbox of the recently activated backup &gt; Edit**[![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/MrmwIfsPDHTNanNM-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/MrmwIfsPDHTNanNM-image.png)
    3. Go to **Configuration** and click on the **Schedules** and set the **First Date** to when backups had started to work and save the changes![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/zCpXC3oLWscbGn8b-image.png)
    4. Go to **Audit &gt; Select the checkbox of the older backup showing "No result" &gt; Merge &gt;** **Select the checkbox of the recently activated backup &gt; Merge into**   
        [![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/p6qCNsbEniG07Ht1-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/p6qCNsbEniG07Ht1-image.png)