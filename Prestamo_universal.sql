/* CREACI�N DE DB */
USE master;
GO

-- Verificar si la base de datos existe y eliminarla si es as�
IF EXISTS
(
    SELECT name
    FROM sys.databases
    WHERE name = 'Prestamo_universal'
)
BEGIN
    -- Eliminar la base de datos existente
    DROP DATABASE Prestamo_universal;
END
GO

-- Crear la base de datos con los archivos de datos y log
BEGIN TRY
    CREATE DATABASE Prestamo_universal ON
    (
        NAME = N'Prestamo_universal_dat',
        FILENAME = N'C:\db\Prestamo_universal_dat.mdf',
        SIZE = 10MB,
        MAXSIZE = 50MB,
        FILEGROWTH = 5MB
    )
    LOG ON
    (
        NAME = N'Prestamo_universal_log',
        FILENAME = N'C:\db\Prestamo_universal_log.ldf',
        SIZE = 5MB,
        MAXSIZE = UNLIMITED,
        FILEGROWTH = 10%
    );
    -- Confirmaci�n de creaci�n
    PRINT 'Base de datos Prestamo_universal creada exitosamente.';
END TRY
BEGIN CATCH
    -- Manejo de errores
    PRINT 'Error al crear la base de datos: ' + ERROR_MESSAGE();
END CATCH;
GO

/*CREACI�N DE TABLAS*/
USE Prestamo_universal;
GO

-- Tabla Tipo Documento
CREATE TABLE Tipo_documento(
	ti_documento CHAR(2) PRIMARY KEY NOT NULL,
	de_larga_tipo_docu VARCHAR(30) NOT NULL,
	de_tipo_docu VARCHAR(15) NOT NULL
);
GO

-- Tabla Pais del Documento
CREATE TABLE Pais_docu(
	id_pais_docu CHAR(4) PRIMARY KEY NOT NULL,
	de_pais_docu VARCHAR(50) NOT NULL
);
GO

-- Tabla Tipo Persona
CREATE TABLE Tipo_persona(
	id_ti_persona CHAR(1) PRIMARY KEY NOT NULL,
	de_ti_persona VARCHAR(16) NOT NULL
);
GO

-- Tabla Profesion u Oficio
CREATE TABLE Profesion(
	id_profesion INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	de_profesion VARCHAR(60) NOT NULL
);
GO

-- Tabla Tipo Sexo
CREATE TABLE Tipo_sexo(
	ti_sexo CHAR(1) PRIMARY KEY NOT NULL,
	de_ti_sexo VARCHAR(9) NOT NULL
);
GO

-- Tabla Estado Civil
CREATE TABLE Estado_civil(
	id_esta_civil INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	de_esta_civil VARCHAR(11) NOT NULL
);
GO

-- Tabla Estado Cliente o Inversionista
CREATE TABLE Estado(
	id_estado CHAR(1) PRIMARY KEY NOT NULL,
	de_estado VARCHAR(11) NOT NULL
);
GO
/*
-- Tabla Ubigeo
CREATE TABLE Ubigeo_domicilio(
	id_ubigeo_domicilio CHAR(6) PRIMARY KEY NOT NULL,
	de_ubigeo_domicilio VARCHAR(20) NOT NULL
);
GO
*/
-- Tabla Categoria Cliente
CREATE TABLE Categoria_cliente(
	id_cat_cliente INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	de_cat_cliente VARCHAR(20) NOT NULL,  /*VALIDAR*/
);
GO

-- Tabla Nivel Inversionista
CREATE TABLE Nivel_inversionista(
	id_niv_inversionista INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	de_niv_inversionista VARCHAR(8) NOT NULL,
);
GO

--Tabla Estado producto: Estado de la inversi�n o pr�stamo
CREATE TABLE Estado_producto(
	id_estado_producto INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	de_estado_producto VARCHAR(30)
)

-- Tabla Maestra Diaria Clientes
CREATE TABLE MD_clientes(
	id_cliente INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	ti_documento CHAR(2) FOREIGN KEY REFERENCES Tipo_documento(ti_documento) NOT NULL,
	nu_documento VARCHAR(15) NOT NULL,
	nombre_cliente NVARCHAR(100) NOT NULL,
	email_cliente NVARCHAR(100),
	telefono_cliente VARCHAR(15),
	direccion_cliente NVARCHAR(200),
	--id_ubigeo_domicilio CHAR(6) FOREIGN KEY REFERENCES Ubigeo_domicilio(id_ubigeo_domicilio) NOT NULL,
	id_pais_docu CHAR(4) FOREIGN KEY REFERENCES Pais_docu(id_pais_docu) NOT NULL,
	id_ti_persona CHAR(1) FOREIGN KEY REFERENCES Tipo_persona(id_ti_persona),
	ti_sexo CHAR(1) FOREIGN KEY REFERENCES Tipo_sexo(ti_sexo),
	fe_nacimiento DATE,
	id_profesion INT FOREIGN KEY REFERENCES Profesion(id_profesion),
	id_esta_civil INT FOREIGN KEY REFERENCES Estado_civil(id_esta_civil),
	id_estado CHAR(1) FOREIGN KEY REFERENCES Estado(id_estado) NOT NULL,
	id_cat_cliente INT FOREIGN KEY REFERENCES Categoria_cliente(id_cat_cliente) NOT NULL,
	fe_apertura  DATE NOT NULL DEFAULT GETDATE(),
	fe_aper_prim_prest DATE NOT NULL DEFAULT GETDATE(),
	fe_actu_reg DATE NOT NULL DEFAULT GETDATE()
);
GO

-- �ndice en n�mero de documento
CREATE INDEX idx_nu_documento_cliente ON MD_clientes(nu_documento);

-- �ndice en email del cliente
CREATE INDEX idx_email_cliente ON MD_clientes(email_cliente);

-- �ndice en estado del cliente
CREATE INDEX idx_estado_cliente ON MD_clientes(id_estado);

-- Tabla Maestra Diaria Inversionistas
CREATE TABLE MD_inversionistas(
	id_inversionista INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
	ti_documento CHAR(2) FOREIGN KEY REFERENCES Tipo_documento(ti_documento) NOT NULL,
	nu_documento VARCHAR(15) NOT NULL,
	nombre_inversionista VARCHAR(100) NOT NULL,
	email_inversionista VARCHAR(100),
	telefono_inversionista VARCHAR(15),
	direccion_inversionista VARCHAR(200),
	--id_ubigeo_domicilio CHAR(6) FOREIGN KEY REFERENCES Ubigeo_domicilio(id_ubigeo_domicilio) NOT NULL,
	id_pais_docu CHAR(4) FOREIGN KEY REFERENCES Pais_docu(id_pais_docu) NOT NULL,
	id_ti_persona CHAR(1) FOREIGN KEY REFERENCES Tipo_persona(id_ti_persona) NOT NULL,
	ti_sexo CHAR(1) FOREIGN KEY REFERENCES Tipo_sexo(ti_sexo),
	fe_nacimiento DATE,
	id_profesion INT FOREIGN KEY REFERENCES Profesion(id_profesion),
	id_esta_civil INT FOREIGN KEY REFERENCES Estado_civil(id_esta_civil),
	id_estado CHAR(1) FOREIGN KEY REFERENCES Estado(id_estado) NOT NULL,
	id_niv_inversionista INT FOREIGN KEY REFERENCES Nivel_inversionista(id_niv_inversionista) NOT NULL,
	fe_apertura  DATE NOT NULL DEFAULT GETDATE(),
	fe_aper_prim_inver DATE NOT NULL DEFAULT GETDATE(),
	fe_actu_reg DATE NOT NULL DEFAULT GETDATE()
);
GO

-- �ndice en n�mero de documento
CREATE INDEX idx_nu_documento_inversionista ON MD_inversionistas(nu_documento);

-- �ndice en email del inversionista
CREATE INDEX idx_email_inversionista ON MD_inversionistas(email_inversionista);

-- �ndice en estado del inversionista
CREATE INDEX idx_estado_inversionista ON MD_inversionistas(id_estado);

-- Tabla maestra diaria de Prestamos
CREATE TABLE MD_prestamos(
	id_prestamo INT PRIMARY KEY IDENTITY(1,1),
    id_cliente INT FOREIGN KEY REFERENCES MD_clientes(id_cliente),
    monto_prestamo DECIMAL(18, 2) NOT NULL,
    tasa_interes DECIMAL(7, 2) NOT NULL,
    num_cuotas INT NOT NULL,
    fecha_inicio_prestamo DATE NOT NULL,
    --monto_aprobado BIT NOT NULL DEFAULT 0,
	id_estado_producto INT FOREIGN KEY REFERENCES Estado_producto(id_estado_producto),
    fecha_registro DATE NOT NULL DEFAULT GETDATE()
);
GO

-- �ndice en id del cliente
CREATE INDEX idx_id_cliente_prestamo ON MD_prestamos(id_cliente);

-- Tabla Inversiones
CREATE TABLE MD_inversiones (
    id_inversion INT PRIMARY KEY IDENTITY(1,1),
    id_inversionista INT FOREIGN KEY REFERENCES MD_inversionistas(id_inversionista),
    monto_inversion DECIMAL(18, 2) NOT NULL,
    tasa_rendimiento DECIMAL(7, 2) NOT NULL,
    num_desembolsos INT NOT NULL,
    fecha_inicio_inversion DATE NOT NULL,
    --inversion_aprobada BIT NOT NULL DEFAULT 0,
	id_estado_producto INT FOREIGN KEY REFERENCES Estado_producto(id_estado_producto),
    fecha_registro DATE NOT NULL DEFAULT GETDATE()
);
GO

-- �ndice en id del inversionista
CREATE INDEX idx_id_inversionista_inversion ON MD_inversiones(id_inversionista);

-- Tabla Cronogramas_Cuotas
CREATE TABLE Cronogramas_Cuotas (
    id_cronograma INT PRIMARY KEY IDENTITY(1,1),
    id_prestamo INT FOREIGN KEY REFERENCES MD_prestamos(id_prestamo),
    fecha_pago DATE NOT NULL,
    cuota_mensual DECIMAL(18, 2) NOT NULL,
	interes_mensual DECIMAL(18, 2) NOT NULL,
	saldo_pendiente DECIMAL(18, 2) NOT NULL
);
GO

-- �ndice en fecha de pago
CREATE INDEX idx_fecha_pago_cuotas ON Cronogramas_Cuotas(fecha_pago);

-- Tabla Cronogramas_Desembolsos
CREATE TABLE Cronogramas_Desembolsos (
    id_cronograma INT PRIMARY KEY IDENTITY(1,1),
    id_inversion INT FOREIGN KEY REFERENCES MD_inversiones(id_inversion),
    fecha_pago DATE NOT NULL,
    desembolso_mensual DECIMAL(18, 2) NOT NULL,
);
GO

-- �ndice en fecha de pago
CREATE INDEX idx_fecha_pago_desembolsos ON Cronogramas_Desembolsos(fecha_pago);

---------------------------------------------------------------------------------------------------------

/*INSERCI�N DE DATOS INICIALES*/
INSERT INTO Tipo_documento(ti_documento,de_larga_tipo_docu,de_tipo_docu)
VALUES
	('01','LIBRETA ELECTORAL O DNI','L.E / DNI'),
	('04','CARNET DE EXTRANJERIA','CARNET EXT.'),
	('06','REG. UNICO DE CONTRIBUYENTES','RUC'),
	('07','PASAPORTE','PASAPORTE'),
	('11','PART. DE NACIMIENTO-IDENTIDAD','P. NAC.'),
	('00','OTROS','OTROS');

INSERT INTO Pais_docu(id_pais_docu,de_pais_docu)
VALUES
	('9001','BOUVET ISLAND'),
	('9002','COTE D IVOIRE'),
	('9003','FALKLAND ISLANDS (MALVINAS)'),
	('9004','FRANCE, METROPOLITAN'),
	('9005','FRENCH SOUTHERN TERRITORIES'),
	('9006','HEARD AND MC DONALD ISLANDS'),
	('9007','MAYOTTE'),
	('9008','SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS'),
	('9009','SVALBARD AND JAN MAYEN ISLANDS'),
	('9010','UNITED STATES MINOR OUTLYING ISLANDS'),
	('9011','OTROS PAISES O LUGARES'),
	('9013','AFGANISTAN'),
	('9017','ALBANIA'),
	('9019','ALDERNEY'),
	('9023','ALEMANIA'),
	('9026','ARMENIA'),
	('9027','ARUBA'),
	('9028','ASCENCION'),
	('9029','BOSNIA-HERZEGOVINA'),
	('9031','BURKINA FASO'),
	('9037','ANDORRA'),
	('9040','ANGOLA'),
	('9041','ANGUILLA'),
	('9043','ANTIGUA Y BARBUDA'),
	('9047','ANTILLAS HOLANDESAS'),
	('9053','ARABIA SAUDITA'),
	('9059','ARGELIA'),
	('9063','ARGENTINA'),
	('9069','AUSTRALIA'),
	('9072','AUSTRIA'),
	('9074','AZERBAIJAN'),
	('9077','BAHAMAS'),
	('9080','BAHREIN'),
	('9081','BANGLADESH'),
	('9083','BARBADOS'),
	('9087','BELGICA'),
	('9088','BELICE'),
	('9090','BERMUDAS'),
	('9091','BELARUS'),
	('9093','MYANMAR'),
	('9097','BOLIVIA'),
	('9101','BOTSWANA'),
	('9105','BRASIL'),
	('9108','BRUNEI DARUSSALAM'),
	('9111','BULGARIA'),
	('9115','BURUNDI'),
	('9119','BUTAN'),
	('9127','CABO VERDE'),
	('9137','CAIMAN,ISLAS'),
	('9141','CAMBOYA'),
	('9145','CAMERUN,REPUBLICA UNIDA DEL'),
	('9147','CAMPIONE D TALIA'),
	('9149','CANADA'),
	('9155','CANAL (NORMANDAS), ISLAS'),
	('9157','CANTON Y ENDERBURRY'),
	('9159','SANTA SEDE'),
	('9165','COCOS (KEELING),ISLAS'),
	('9169','COLOMBIA'),
	('9173','COMORAS'),
	('9177','CONGO'),
	('9183','COOK, ISLAS'),
	('9187','COREA (NORTE), REPUBLICA POPULAR DEMOCRATICA DE'),
	('9190','COREA (SUR), REPUBLICA DE'),
	('9193','COSTA DE MARFIL'),
	('9196','COSTA RICA'),
	('9198','CROACIA'),
	('9199','CUBA'),
	('9203','CHAD'),
	('9207','CHECOSLOVAQUIA'),
	('9211','CHILE'),
	('9215','CHINA'),
	('9218','TAIWAN (FORMOSA)'),
	('9221','CHIPRE'),
	('9229','BENIN'),
	('9232','DINAMARCA'),
	('9235','DOMINICA'),
	('9239','ECUADOR'),
	('9240','EGIPTO'),
	('9242','EL SALVADOR'),
	('9243','ERITREA'),
	('9244','EMIRATOS ARABES UNIDOS'),
	('9245','ESPANA'),
	('9246','ESLOVAQUIA'),
	('9247','ESLOVENIA'),
	('9249','ESTADOS UNIDOS'),
	('9251','ESTONIA'),
	('9253','ETIOPIA'),
	('9259','FEROE, ISLAS'),
	('9267','FILIPINAS'),
	('9271','FINLANDIA'),
	('9275','FRANCIA'),
	('9281','GABON'),
	('9285','GAMBIA'),
	('9286','GAZA Y JERICO'),
	('9287','GEORGIA'),
	('9289','GHANA'),
	('9293','GIBRALTAR'),
	('9297','GRANADA'),
	('9301','GRECIA'),
	('9305','GROENLANDIA'),
	('9309','GUADALUPE'),
	('9313','GUAM'),
	('9317','GUATEMALA'),
	('9325','GUAYANA FRANCESA'),
	('9327','GUERNSEY'),
	('9329','GUINEA'),
	('9331','GUINEA ECUATORIAL'),
	('9334','GUINEA-BISSAU'),
	('9337','GUYANA'),
	('9341','HAITI'),
	('9345','HONDURAS'),
	('9348','HONDURAS BRITANICAS'),
	('9351','HONG KONG'),
	('9355','HUNGRIA'),
	('9361','INDIA'),
	('9365','INDONESIA'),
	('9369','IRAK'),
	('9372','IRAN, REPUBLICA ISLAMICA DEL'),
	('9375','IRLANDA (EIRE)'),
	('9377','ISLA AZORES'),
	('9378','ISLA DEL MAN'),
	('9379','ISLANDIA'),
	('9380','ISLAS CANARIAS'),
	('9381','ISLAS DE CHRISTMAS'),
	('9382','ISLAS QESHM'),
	('9383','ISRAEL'),
	('9386','ITALIA'),
	('9391','JAMAICA'),
	('9395','JONSTON, ISLAS'),
	('9399','JAPON'),
	('9401','JERSEY'),
	('9403','JORDANIA'),
	('9406','KAZAJSTAN'),
	('9410','KENIA'),
	('9411','KIRIBATI'),
	('9412','KIRGUIZISTAN'),
	('9413','KUWAIT'),
	('9418','LABUN'),
	('9420','LAOS, REPUBLICA POPULAR DEMOCRATICA DE'),
	('9426','LESOTHO'),
	('9429','LETONIA'),
	('9431','LIBANO'),
	('9434','LIBERIA'),
	('9438','LIBIA'),
	('9440','LIECHTENSTEIN'),
	('9443','LITUANIA'),
	('9445','LUXEMBURGO'),
	('9447','MACAO'),
	('9448','MACEDONIA'),
	('9450','MADAGASCAR'),
	('9453','MADEIRA'),
	('9455','MALAYSIA'),
	('9458','MALAWI'),
	('9461','MALDIVAS'),
	('9464','MALI'),
	('9467','MALTA'),
	('9469','MARIANAS DEL NORTE, ISLAS'),
	('9472','MARSHALL, ISLAS'),
	('9474','MARRUECOS'),
	('9477','MARTINICA'),
	('9485','MAURICIO'),
	('9488','MAURITANIA'),
	('9493','MEXICO'),
	('9494','MICRONESIA, ESTADOS FEDERADOS DE'),
	('9495','MIDWAY ISLAS'),
	('9496','MOLDAVIA'),
	('9497','MONGOLIA'),
	('9498','MONACO'),
	('9501','MONTSERRAT, ISLA'),
	('9505','MOZAMBIQUE'),
	('9507','NAMIBIA'),
	('9508','NAURU'),
	('9511','NAVIDAD (CHRISTMAS), ISLA'),
	('9517','NEPAL'),
	('9521','NICARAGUA'),
	('9525','NIGER'),
	('9528','NIGERIA'),
	('9531','NIUE, ISLA'),
	('9535','NORFOLK, ISLA'),
	('9538','NORUEGA'),
	('9542','NUEVA CALEDONIA'),
	('9545','PAPUASIA NUEVA GUINEA'),
	('9548','NUEVA ZELANDA'),
	('9551','VANUATU'),
	('9556','OMAN'),
	('9566','PACIFICO, ISLAS DEL'),
	('9573','PAISES BAJOS'),
	('9576','PAKISTAN'),
	('9578','PALAU, ISLAS'),
	('9579','TERRITORIO AUTONOMO DE PALESTINA.'),
	('9580','PANAMA'),
	('9586','PARAGUAY'),
	('9589','PERU'),
	('9593','PITCAIRN, ISLA'),
	('9599','POLINESIA FRANCESA'),
	('9603','POLONIA'),
	('9607','PORTUGAL'),
	('9611','PUERTO RICO'),
	('9618','QATAR'),
	('9628','REINO UNIDO'),
	('9629','ESCOCIA'),
	('9633','REPUBLICA ARABE UNIDA'),
	('9640','REPUBLICA CENTROAFRICANA'),
	('9644','REPUBLICA CHECA'),
	('9645','REPUBLICA DE SWAZILANDIA'),
	('9646','REPUBLICA DE TUNEZ'),
	('9647','REPUBLICA DOMINICANA'),
	('9660','REUNION'),
	('9665','ZIMBABWE'),
	('9670','RUMANIA'),
	('9675','RUANDA'),
	('9676','RUSIA'),
	('9677','SALOMON, ISLAS'),
	('9685','SAHARA OCCIDENTAL'),
	('9687','SAMOA OCCIDENTAL'),
	('9690','SAMOA NORTEAMERICANA'),
	('9695','SAN CRISTOBAL Y NIEVES'),
	('9697','SAN MARINO'),
	('9700','SAN PEDRO Y MIQUELON'),
	('9705','SAN VICENTE Y LAS GRANADINAS'),
	('9710','SANTA ELENA'),
	('9715','SANTA LUCIA'),
	('9720','SANTO TOME Y PRINCIPE'),
	('9728','SENEGAL'),
	('9731','SEYCHELLES'),
	('9735','SIERRA LEONA'),
	('9741','SINGAPUR'),
	('9744','SIRIA, REPUBLICA ARABE DE'),
	('9748','SOMALIA'),
	('9750','SRI LANKA'),
	('9756','SUDAFRICA, REPUBLICA DE'),
	('9759','SUDAN'),
	('9764','SUECIA'),
	('9767','SUIZA'),
	('9770','SURINAM'),
	('9773','SAWSILANDIA'),
	('9774','TADJIKISTAN'),
	('9776','TAILANDIA'),
	('9780','TANZANIA, REPUBLICA UNIDA DE'),
	('9783','DJIBOUTI'),
	('9786','TERRITORIO ANTARTICO BRITANICO'),
	('9787','TERRITORIO BRITANICO DEL OCEANO INDICO'),
	('9788','TIMOR DEL ESTE'),
	('9800','TOGO'),
	('9805','TOKELAU'),
	('9810','TONGA'),
	('9815','TRINIDAD Y TOBAGO'),
	('9816','TRISTAN DA CUNHA'),
	('9820','TUNICIA'),
	('9823','TURCAS Y CAICOS, ISLAS'),
	('9825','TURKMENISTAN'),
	('9827','TURQUIA'),
	('9828','TUVALU'),
	('9830','UCRANIA'),
	('9833','UGANDA'),
	('9840','URSS'),
	('9845','URUGUAY'),
	('9847','UZBEKISTAN'),
	('9850','VENEZUELA'),
	('9855','VIET NAM'),
	('9858','VIETNAM (DEL NORTE)'),
	('9863','VIRGENES, ISLAS (BRITANICAS)'),
	('9866','VIRGENES, ISLAS (NORTEAMERICANAS)'),
	('9870','FIJI'),
	('9873','WAKE, ISLA'),
	('9875','WALLIS Y FORTUNA, ISLAS'),
	('9880','YEMEN'),
	('9885','YUGOSLAVIA'),
	('9888','ZAIRE'),
	('9890','ZAMBIA'),
	('9895','ZONA DEL CANAL DE PANAMA'),
	('9896','ZONA LIBRE OSTRAVA'),
	('9897','ZONA NEUTRAL (PALESTINA)');

INSERT INTO Tipo_persona(id_ti_persona,de_ti_persona)
VALUES
	('1','PERSONA NATURAL'),
	('2','PERSONA JUR�DICA');

SET IDENTITY_INSERT Profesion ON;

INSERT INTO Profesion(id_profesion,de_profesion)
VALUES
	(1,'ABOGADO'),
	(2,'ACTOR, ARTISTA Y DIRECTOR DE ESPECTACULOS'),
	(3,'ADMINISTRADOR DE EMPRESAS (PROFESIONAL)'),
	(4,'AGRIMENSOR Y TOPOGRAFO'),
	(5,'AGR�NOMO'),
	(6,'ALBANIL'),
	(7,'ANALISTAS DE SISTEMA Y COMPUTACION'),
	(8,'ANTROPOLOGO, ARQUEOLOGO Y ETNOLOGO'),
	(9,'ARQUITECTO'),
	(10,'ARTESANO DE CUERO'),
	(11,'ARTESANO TEXTIL'),
	(12,'AUTOR LITERARIO, ESCRITOR Y CRITICO'),
	(13,'BACTERIOLOGO, FARMACOLOGO'),
	(14,'BIOLOGO'),
	(15,'CARPINTERO'),
	(16,'CONDUCTOR DE VEHICULOS DE MOTOR'),
	(17,'CONTADOR'),
	(18,'COREOGRAFO Y BAILARINES'),
	(19,'COSMETOLOGO, PELUQUERO Y BARBERO'),
	(20,'DECORADOR, DIBUJANTE, PUBLICISTA, DISE�ADOR DE PUBLICIDAD'),
	(21,'DEPORTISTA PROFESIONAL Y ATLETA'),
	(22,'DIRECTOR DE EMPRESAS'),
	(23,'ECONOMISTA'),
	(24,'ELECTRICISTA (TECNICO)'),
	(25,'ENFERMERO'),
	(26,'ENTRENADOR DEPORTIVO'),
	(27,'ESCENOGRAFO'),
	(28,'ESCULTOR'),
	(29,'ESPECIALISTA EN TRATAMIENTO DE BELLEZA'),
	(30,'FARMACEUTICO '),
	(31,'FOTOGRAFO Y OPERADORES CAMARA, CINE Y TV'),
	(32,'GASFITERO'),
	(33,'GEOGRAFO'),
	(34,'INGENIERO'),
	(35,'INTERPRETE, TRADUCTOR, FILOSOFO'),
	(36,'JOYERO Y/O PLATERO'),
	(37,'LABORATORISTA (TECNICO)'),
	(38,'LOCUTOR DE RADIO, TV'),
	(39,'MECANICO MOTORES AVIONES Y NAVES MARINAS'),
	(40,'MECANICO DE VEHICULOS DE MOTOR'),
	(41,'MEDICO Y CIRUJANO'),
	(42,'MODELO'),
	(43,'MUSICO'),
	(44,'NUTRICIONISTA'),
	(45,'OBSTETRIZ'),
	(46,'ODONTOLOGO'),
	(47,'PERIODISTA'),
	(48,'PILOTO DE AERONAVES'),
	(49,'PINTOR'),
	(50,'PROFESOR'),
	(51,'PSICOLOGO'),
	(52,'RADIO TECNICO'),
	(53,'REGIDORES DE MUNICIPALIDADES'),
	(54,'RELACIONISTA PUBLICO E INDUSTRIAL'),
	(55,'SASTRE'),
	(56,'SOCIOLOGO'),
	(57,'TAPICERO'),
	(58,'TAXIDERMISTA, DISECADOR DE ANIMALES'),
	(59,'VETERINARIO'),
	(60,'PODOLOGOS'),
	(61,'ARCHIVERO'),
	(62,'ALBACEA'),
	(63,'GESTOR DE NEGOCIO'),
	(64,'MANDATARIO'),
	(65,'SINDICO'),
	(66,'TECNOLOGOS MEDICOS'),
	(67,'PROFESION U OCUPACION NO ESPECIFICADA ');

SET IDENTITY_INSERT Profesion OFF;

INSERT INTO Tipo_sexo(ti_sexo, de_ti_sexo)
VALUES
	('F','FEMENINO'),
	('M','MASCULINO');


SET IDENTITY_INSERT Estado_civil ON;

INSERT INTO Estado_civil(id_esta_civil, de_esta_civil)
VALUES
	(1,'SOLTERO'),
	(2,'CONVIVIENTE'),
	(3,'DIVORCIADO'),
	(4,'SEPARADO'),
	(5,'DIVORCIADO'),
	(6,'VIUDO');

SET IDENTITY_INSERT Estado_civil OFF;

INSERT INTO Estado(id_estado,de_estado)
VALUES
	('B','BAJA'),
	('K','BLOQUEADO'),
	('O','PREVIO BAJA'),
	('V','VIGENTE');


SET IDENTITY_INSERT Categoria_cliente ON;

INSERT INTO Categoria_cliente(id_cat_cliente,de_cat_cliente)
VALUES
	(1,'F'),
	(2,'D'),
	(3,'D+'),
	(4,'C-'),
	(5,'C'),
	(6,'C+'),
	(7,'B-'),
	(8,'B'),
	(9,'B+'),
	(10,'A-'),
	(11,'A');

SET IDENTITY_INSERT Categoria_cliente OFF;


SET IDENTITY_INSERT Nivel_inversionista ON;

INSERT INTO Nivel_inversionista(id_niv_inversionista,de_niv_inversionista)
VALUES
	(5,'BRONCE'),
	(4,'PLATA'),
	(3,'ORO'),
	(2,'PLATINO'),
	(1,'DIAMANTE');

SET IDENTITY_INSERT Nivel_inversionista OFF;

SET IDENTITY_INSERT Estado_producto ON;

INSERT INTO Estado_producto(id_estado_producto,de_estado_producto)
VALUES
	(1, 'APROBADO'),
	(2, 'RECHAZADO'),
	(3, 'PENDIENTE DE APROBACI�N');

SET IDENTITY_INSERT Estado_producto OFF;
