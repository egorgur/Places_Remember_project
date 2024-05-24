Memorizer
===
https://memorizer.testotheca.online

This web-site allows to store your memories about any places in the world

Features
===

- Social-network Vkontakte authorization
- View all your memories & individual ones
- Add new memory and point a place it's mark on the map
- Edit a memory
- Delete a memory

### Authorization

The authorization process includes granting access to your Vkontakte account main data (only first name; last name; profile photo) 

![image](https://github.com/egorgur/Places_Remember_project/assets/122800013/bed54139-25f3-41e2-9a2c-72afc2e080e3)

After the authorization your account data will be shown on the main page 

### Main page

This page shows all your memories

you can make new memory or open the view-memory page and edit/delete the existing ones

![image](https://github.com/egorgur/Places_Remember_project/assets/122800013/25474316-2188-4cb8-a127-98c91cc29c59)


also you can leave your account and be redirected onto the authorization page

![image](https://github.com/egorgur/Places_Remember_project/assets/122800013/f79093c0-4f8e-4676-a7cb-b7abbc895b3f)


### What's the memory?

The memory is an object that contains:

- map point coordinates
- name of the memory
- text of the memory

![image](https://github.com/egorgur/Places_Remember_project/assets/122800013/0ae724fb-9944-4497-8f59-66997063e145)


Edit/delete memory

![image](https://github.com/egorgur/Places_Remember_project/assets/122800013/bde2b99a-e5ad-435a-ab78-adde97a97f02)


Technologies used in the project
===

- Database: **PostgreSQL** | _stores memories and users data_
- Web-Framework: **Django** | _web framework_
- Frontend: html js scss | _basic Frontend_
- Git-Actions: Django Tests & Ruff linter | run tests and lint checks on push

Known Issues
===
- First authorization page load very slow because it loads Js Vk SDK module
