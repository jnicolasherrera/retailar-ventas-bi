
-- Tabla DimProducto
IF OBJECT_ID('ventas.DimProducto', 'U') IS NOT NULL DROP TABLE ventas.DimProducto;
GO
CREATE TABLE ventas.DimProducto (
    id_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(150),
    categoria VARCHAR(100),
    costo DECIMAL(18, 2)
);
GO

-- Tabla DimSucursal
IF OBJECT_ID('ventas.DimSucursal', 'U') IS NOT NULL DROP TABLE ventas.DimSucursal;
GO
CREATE TABLE ventas.DimSucursal (
    id_sucursal INT PRIMARY KEY,
    nombre_sucursal VARCHAR(150),
    provincia VARCHAR(100),
    region VARCHAR(100)
);
GO

-- Tabla FactVentas
IF OBJECT_ID('ventas.FactVentas', 'U') IS NOT NULL DROP TABLE ventas.FactVentas;
GO
CREATE TABLE ventas.FactVentas (
    id_venta INT IDENTITY(1,1) PRIMARY KEY,
    fecha_venta DATE NOT NULL,
    id_sucursal INT,
    id_producto INT,
    cantidad INT,
    precio_unitario DECIMAL(18, 2),
    canal_venta VARCHAR(100),
    FOREIGN KEY (id_producto) REFERENCES ventas.DimProducto(id_producto),
    FOREIGN KEY (id_sucursal) REFERENCES ventas.DimSucursal(id_sucursal)
);
GO
