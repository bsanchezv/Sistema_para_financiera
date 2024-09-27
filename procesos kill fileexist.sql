-- Mostrar los procesos que est�n utilizando la base de datos
EXEC sp_who2;
GO

Kill 52;


EXEC xp_fileexist 'C:\Bases\Clientes.csv';