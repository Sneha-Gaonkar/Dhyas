# EManagementDemo
***Task accomplished till date***
1. Login and Signup page functionality.
2. Admin can login as admin if the credentials matches and will apparently get access for admin panel.
3. User can login as user if the credentials matches and will apparently get access for user dashboard.
4. User can signup if he is not done with creating account procedure.
5. If a new user signups the notifications will be sent to admin spontaneously.
6. I have created 3 dummy admins who will be having specific database allotted.
7. If a new user is creating a account or is in midst of signup process the approval of admin will allow the new user to create a account.
8. Refusal of admin will deprive or restrict the user from creating account.
9. Here till date the notifications are being received at admin end but all the admins are getting the notifications.
10. After admin approval the credentials will be inserted in signup as well as login table along with account creating time simultaneously.
11. The UserID, Username, System IPAdress, Logintime will be inserted in loginlogs table as soon as login is done. 
12. Fetching of Voterlist, Sorting, etc. is well and good and is going hand in hand.
13. Whatsapp is also functional but just the data is being sent like the voters details.
14. In the UI there is PartNo range selecting drop down, there if the PartNo is in first column then only the PartNo wise sorting is successfully done.

***Task required to be accomplished***
1. The notifications should be proceeded to database-alloted admin only.
   Eg: If the user who is in midst of signup process is choosing database name as Panvel then the admin with Panvel database access only should receive notifications.
2. If the admin is approving or even refusing that notifications should be sent to user end.
3. The image should also be sent of the leader for whom vote is done in whatsapp along with voter details to the voter candidate.
4. After selecting partNo range the sorting is not done sequencely.
   Eg: If PartNo selection range is from 1 to 4 then first PartNo 1 then 3 then 2 then 4 is getting displayed, but it should be in sequence.
