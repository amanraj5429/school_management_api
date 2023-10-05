# school_management_api

This is a role based crud operation for multiple endpoints.

The Endpoints are:

USER Endpoints--------------------------------------------------------------------------

GET-http://127.0.0.1:5000/users-- returns all the users present

POST-http://127.0.0.1:5000/users -- you can add new user by passing name and role in form of json object

PUT-http://127.0.0.1:5000/user/userid -- you can pass userid which you want to update with the values which you want to update

DELETE- http://127.0.0.1:5000/user/7 -- you can pass the user id which you want to delete

SUBJECT Endpoints------------------------------------------------------------------------------------------------

GET-http://127.0.0.1:5000/read_subject?user_id=user_id of principal -- returns all the subjects present

POST- http://127.0.0.1:5000/create_subject?user_id=user_id of vice-principal -- adds new subject, you just have to pass subject name in form of json object and user-id of vice-principal.

PUT- http://127.0.0.1:5000/update_subject/subject_id?user_id=user_id of vice-principal -- Update the existing subject, you just have to pass the required subject_id which you want to update and the required values for it in json object when you give user-id of vice-principal.

DELETE-http://127.0.0.1:5000/update_subject/subject_id?user_id=user_id of principal -- Delete the given subject corresponding to the subject id when the corresponding user id of principal

TIMETABLE Endpoints---------------------------------------------------------------------------------------------

GET- http://127.0.0.1:5000/read_timetables?user_id=user_id of principal -- returns all the timetables present when user_id of principal is given.

POST - http://127.0.0.1:5000/add_timetables?user_id=user_id of vice-principal -- Adds new time-table when user-id of vice-principal is given.

PUT- http://127.0.0.1:5000/update_timetables/time_table_id?user_id=user_id of vice-principal -- Updates the given time-table for the corresponding time-table id you just have to pass time-table id, required new values in form of json object and user_id of vice principal user.

DELETE - http://127.0.0.1:5000/delete_timetables/time_table_id?user_id=user_id of principal -- Deletes the corresponding Time-table of the given time-table id when user-id of principal is given.


ALLOCATION Endpoints----------------------------------------------------------------------------------------------

GET - http://127.0.0.1:5000/read_allocate_subject?user_id=user_id of principal -- returns all the allocated subjects when user id of principal is given.

POST -  http://127.0.0.1:5000/allocate_subject?user_id=user_id of vice-principal -- add new allocated subject when user id of vice principal is given, you just have to pass existing subject-id and existing time-table id in form of json object.

PUT - http://127.0.0.1:5000/update_allocations/allocated_id?user_id=user_id of vice-principal -- Updates the given allocated subject corresponding to allocation_id provided when given user_id of vice-principal is given, you just have to pass new existing time-table id and new existing subject-id in form of json object.

DELETE- http://127.0.0.1:5000/delete_allocations/allocated_id?user_id=user_id of principal -- Deletes the corresponding Allocated-subject for the id of allocated subject is provided, when provided user id of principal.

Teachers Endpoint------------------------------------------------------------------------------------------------------

GET - http://127.0.0.1:5000/teachers?user_id=user_id of teacher -- returns all teachers when user_id of teacher is given


