USE Prestamo_universal;
GO
CREATE TABLE #temp_clientes(
	ti_documento CHAR(2),
	nu_documento VARCHAR(15),
	nombre_cliente NVARCHAR(100),
	email_cliente NVARCHAR(100),
	telefono_cliente VARCHAR(15),
	direccion_cliente NVARCHAR(200),
	id_pais_docu CHAR(4),
	id_ti_persona CHAR(1),
	ti_sexo CHAR(1),
	fe_nacimiento DATE,
	nu_cant_pres INT,
	id_profesion INT,
	id_esta_civil INT,
	id_estado CHAR(1),
	id_cat_cliente INT
);
-- Cargar los clientes sin la columna id_cliente
BEGIN TRY
	BULK INSERT #temp_clientes
	FROM 'C:\Users\User\Desktop\Disco D\My_Projects\Prestamo_universal\Bases\Clientes.csv'
	WITH 
	(
    FIELDTERMINATOR = ';',  
    ROWTERMINATOR = '\n',
    FIRSTROW = 2,           
    CODEPAGE = '65001',
    TABLOCK
	);

END TRY
BEGIN CATCH
    SELECT ERROR_MESSAGE() AS PincheError;
END CATCH;

INSERT INTO Prestamo_universal.dbo.MD_clientes
(ti_documento, nu_documento, nombre_cliente, email_cliente, telefono_cliente, direccion_cliente, id_pais_docu, id_ti_persona, ti_sexo, fe_nacimiento, nu_cant_pres, id_profesion, id_esta_civil, id_estado, id_cat_cliente)
SELECT ti_documento, nu_documento, nombre_cliente, email_cliente, telefono_cliente, direccion_cliente, id_pais_docu, id_ti_persona, ti_sexo, fe_nacimiento, nu_cant_pres, id_profesion, id_esta_civil, id_estado, id_cat_cliente
FROM #temp_clientes;


SELECT * FROM #temp_clientes;

SELECT * FROM Prestamo_universal.dbo.MD_clientes;

DROP TABLE #temp_clientes;