

SyncSign Single Sign-On (SSO) System
=================================

This is a simple Single Sign-On (SSO) system implemented using Flask, a lightweight web framework in Python. This SSO system allows users to log in once and access multiple applications without the need to log in again.

Features
--------

*   Users can log in with their username and password.
*   Session-based authentication to keep users logged in across multiple requests.
*   Demonstrates how to protect routes for multiple applications with SSO.


Run
------

`app.py` is the server file run however you want


Usage
-----

1.  Set up a secret key for the Flask app. Open `app.py` and replace `'your_secret_key'` with a random secret key.
2.  Run the Flask app:
`python app.py`4.  Access the application in your web browser at `http://localhost:5000`.

How it Works
------------

*   **Login:** Users can log in with their username and password. The credentials are validated against a database of users.
*   **Session:** After successful login, the user's username is stored in the session to keep them logged in across requests.
*   **Protected Routes:** The SSO system includes appID for  applications (`signin/app_id` and `signin/app_id`). User Can login with those url. If a user is authenticated, they will be redirected to the respective application. Otherwise, they will see a message indicating that they are not logged in.

Contributing
------------

Contributions are welcome! Feel free to open issues or pull requests.

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.