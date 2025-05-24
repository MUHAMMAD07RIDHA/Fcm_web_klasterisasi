# Proyek FCM 
nstallation
Clone this repository.
Install the dependencies. Run composer install command.
Create .env file by simply copying the .env.example file and rename it.
Configure the .env file with your database connection, seeder configuration, etc.
Generate the application key with php artisan key:generate command.
Generate the storage link with php artisan storage:link command.
Generate the database structure with this commands based on your preferences:
Use php artisan migrate for creating / updating the database.
Use php artisan db:seed for seeding the database.
Use php artisan migrate:fresh for fresh installation.
Use php artisan migrate:fresh --seed for fresh installation and seeding the database.
Warning! If you use php artisan migrate:fresh command, all tables will be dropped and recreated. All data in the tables will be lost.

Finally, start the application with php artisan serve command
