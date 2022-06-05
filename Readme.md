# [InstagramTypeApi](https://sid-social.herokuapp.com/docs) 

InstagramTypeApi is a simple social media api using fastapi, sqlalchemy, alembic and postgresql , which supports user authentication(signup with profile photo and email verification otp, signin) using jwt token ,when anyone or user signed-in then a sign in alert received by user email ,
sign in user can create post with multiple photos and also user can comment on any post,user can delete only own post, also get all post.


#Features 

- [Create User & Automatically sent an email verification otp](https://sid-social.herokuapp.com/docs#/Users/create_users_users_post)

- [Email Verification](https://sid-social.herokuapp.com/docs#/Users/email_verification_users_email_verify_get):- Without email 
verification you can not sign in

- [Resend OTP](https://sid-social.herokuapp.com/docs#/Users/resend_users_resend_otp_post):- if you have not received any email then you can again request to sent an otp to your email 

- [Sign in & sent an login alert to your email](https://sid-social.herokuapp.com/docs#/Authentication/login_login_post)

- [Get All Posts](https://sid-social.herokuapp.com/docs#/Posts/posts_post_all_get)

- [Create Post ](https://sid-social.herokuapp.com/docs#/Posts/create_post_post_post)

- [Upload photos of your post](https://sid-social.herokuapp.com/docs#/Posts/upload_image_post_image_post)

- [Delete Own Post](https://sid-social.herokuapp.com/docs#/Posts/delete_post_post_delete__id__get)

- [Comment on Any Post](https://sid-social.herokuapp.com/docs#/Comments/create_comments_post)

- [Get all Comments of specific post](https://sid-social.herokuapp.com/docs#/Comments/commments_comments_all__post_id__get)



## I Mainly Used 

- FastApi Framework
- Postgresql as a database
- alembic as db migration tool
- Pyscopg2 Driver
- Sqlalchemy Orm
- passlib[Bcrypt] For Hashing Password
- python-jose[Cryptography] for creating JWT token
- aiofiles for making Image directory statically avialable
- Jinja2 for template
- fastapi-mail for sending mail
- Heroku for deploying
