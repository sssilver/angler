angler
======

Installation notes
------------------
On first install, for the admin user, run the following:
`sqlite3 /opt/data/angler.db "insert into staff(email, password) values('[email]', '[password]')"`

Passwords are not encrypted yet.