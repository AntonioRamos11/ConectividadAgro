CREATE PROCEDURE AgregarSucursal
    @id_sucursal INT,
    @nombre_sucursal NVARCHAR(50),
    @direccion_sucursal NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Sucursal (id_sucursal, nombre_sucursal, direccion_sucursal)
    VALUES (@id_sucursal, @nombre_sucursal, @direccion_sucursal)
END

CREATE PROCEDURE EliminarEmpleado
    @id_empleado INT
AS
BEGIN
    DELETE FROM Empleado
    WHERE id_empleado = @id_empleado;
END;
GO


CREATE PROCEDURE EliminarSucursal
    @id_sucursal INT
AS
BEGIN
    SET NOCOUNT ON;
    DELETE FROM Sucursal
    WHERE id_sucursal = @id_sucursal
END



CREATE PROCEDURE ActualizarSucursal
    @id_sucursal INT,
    @nuevo_nombre NVARCHAR(50),
    @nueva_direccion NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    UPDATE Sucursal
    SET nombre_sucursal = @nuevo_nombre,
        direccion_sucursal = @nueva_direccion
    WHERE id_sucursal = @id_sucursal
END


CREATE PROCEDURE ConsultarSucursales
    @filtro NVARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;
    SELECT id_sucursal, nombre_sucursal, direccion_sucursal
    FROM Sucursal
    WHERE nombre_sucursal LIKE '%' + @filtro + '%'
END

use Agroquimicos
Go
DROP PROCEDURE ActualizarPuestoEmpleado
Go
CREATE PROCEDURE ActualizarPuestoEmpleado
    @id_empleado INT,
    @nuevo_puesto NVARCHAR(50)
AS
BEGIN
    -- Verificar si el empleado pertenece a un CEDIS
    DECLARE @id_cedis INT;
    SELECT @id_cedis = id_cedis FROM Empleado WHERE id_empleado = @id_empleado;

    -- Validar que no se puede asignar "Vendedor" si pertenece a un CEDIS
    IF @nuevo_puesto = 'Vendedor' AND @id_cedis IS NOT NULL
    BEGIN
        RAISERROR('No se puede asignar "Vendedor" a un empleado que pertenece a un CEDIS.', 16, 1);
        RETURN;
    END

    -- Actualizar el puesto
    UPDATE Empleado
    SET puesto_empleado = @nuevo_puesto
    WHERE id_empleado = @id_empleado;
END;
