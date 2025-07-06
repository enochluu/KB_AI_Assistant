https://knowledgebase.emergingit.com.au/books/backup-errors-and-fixes/page/replication-session-does-not-exist
# Replication session does not exist

## **Issue**

You may encounter the following error when attempting to replicate a protected machine:

```
Replication session 'bd5f3879-83c5-41c9-806c-b23bce57d25a' does not exist
```

This typically occurs when the replication session has become stale or disconnected and needs to be manually restarted. Restarting the replication job usually resolves the issue first try.

---

## **Cause**

This error is usually caused by a temporary communication issue between the source Core and the replication target, or due to a session timeout. It does not typically indicate a critical failure but requires manual intervention to resume replication.

---

## **Resolution**

### **Restart the replication session:**

1. Open the **Quest Rapid Recovery Console**.
2. Click the **Replication** icon on the top left as shown here
    
    [![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/7rnzDI0cSdUNGk7I-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/7rnzDI0cSdUNGk7I-image.png)
3. Locate the server experiencing the issue by expanding the list of replicated servers.
4. **Check the box** next to the server name.
5. Click the **"Force"** button to manually restart the replication session.
    
    [![image.png](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/scaled-1680-/NiDJMfMyZLkdWQ43-image.png)](https://knowledgebase.emergingit.com.au/uploads/images/gallery/2025-05/NiDJMfMyZLkdWQ43-image.png)