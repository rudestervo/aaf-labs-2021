#include <iostream>
#include "Token.h"
#include "Database.h"

using namespace std;

int main()
{
	setlocale(LC_ALL, "RU");

	Database database;
	
	start(database, "CREATE owners (owner_id INDEXED, owner_name, owner_age)");
	
	start(database, "INSERT INTO owners (`1`, `Ivan`, `20`)");

	start(database, "INSERT INTO owners (`2`, `Petya`, `21`)");

	start(database, "INSERT INTO owners (`3`, `Vanya`, `19`)");

	start(database, "SELECT owner_name, owner_age FROM owners");

	start(database, "CREATE cats (cat_id INDEXED, cat_owner_id INDEXED, cat_name)");

	start(database, "INSERT INTO cats (`1`, `1`, `Bella`)");

	start(database, "INSERT INTO cats (`2`, `2`, `Leo`)");

	start(database, "INSERT INTO cats (`3`, `3`, `Jack`)");

	start(database, "SELECT cat_name FROM cats WHERE cat_owner_id = `2`");

	start(database, "SELECT cat_name, owner_name FROM cats JOIN owners");

	start(database, "SELECT cat_name, owner_name FROM cats JOIN owners ON cat_owner_id = owner_id");

	start(database, "SELECT cat_name, owner_name FROM cats JOIN owners ON cat_owner_id = owner_id WHERE owner_id = `1`");

	start(database, "SELECT cat_name FROM cats WHERE cat_owner_id >= `2`");

	start(database, "DELETE FROM owners WHERE owner_id = `1`");

	start(database, "SELECT owner_id FROM owners WHERE owner_id != `4`");
	
	return 0;
}