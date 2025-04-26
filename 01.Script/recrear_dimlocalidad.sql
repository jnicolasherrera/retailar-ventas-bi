
/*‑‑‑ 1. Cambiás contexto a la base correcta ‑‑‑*/
USE RetailAR;
GO

/*‑‑‑ 2. Si quedó una vista “huérfana”, la eliminás ‑‑‑*/
IF OBJECT_ID('ventas.vw_FactVentasEnriquecida', 'V') IS NOT NULL
    DROP VIEW ventas.vw_FactVentasEnriquecida;
GO

ALTER TABLE ventas.DimTipoCambio
ALTER COLUMN fecha date;



USE RetailAR;
GO
DROP VIEW IF EXISTS ventas.vw_FactVentasEnriquecida;
GO

CREATE VIEW ventas.vw_FactVentasEnriquecida AS
SELECT
      v.fecha_venta
    , v.id_sucursal
    , v.id_producto
    , v.cantidad
    , v.precio_unitario
    , v.canal_venta
    , pr.nombre_producto          AS nombre_producto
    , pr.categoria
    , pr.costo
    , su.nombre_sucursal          AS nombre_sucursal
    , su.provincia
    , su.region
    , tc.tipo_cambio_oficial      AS tipo_cambio_oficial
    , loc.latitud
    , loc.longitud
    , v.cantidad * v.precio_unitario                     AS ImporteARS
    , v.cantidad * pr.costo                              AS CostoTotalARS
    , v.cantidad * v.precio_unitario / tc.tipo_cambio_oficial AS ImporteUSD
    , (v.cantidad * v.precio_unitario) - (v.cantidad * pr.costo) AS MargenARS
FROM ventas.FactVentas      AS v
JOIN ventas.DimProducto     AS pr  ON v.id_producto  = pr.id_producto
JOIN ventas.DimSucursal     AS su  ON v.id_sucursal  = su.id_sucursal
LEFT JOIN ventas.DimTipoCambio  AS tc  
       ON v.fecha_venta = CAST(tc.fecha AS date)      -- casteo para que coincidan tipos
LEFT JOIN ventas.DimLocalidad   AS loc 
       ON su.provincia       = loc.provincia
      AND su.nombre_sucursal = loc.ciudad;
GO


SELECT  MIN(fecha_venta) AS FechaMin,
        MAX(fecha_venta) AS FechaMax
FROM    ventas.FactVentas;

DECLARE @min date = '2023-01-01',
        @max date = '2024-12-31';

;WITH fechas AS (
    SELECT @min AS d
    UNION ALL
    SELECT DATEADD(DAY,1,d) FROM fechas WHERE d < @max
)
SELECT d AS FechaFaltante
FROM   fechas f
LEFT  JOIN ventas.DimTipoCambio tc ON tc.fecha = f.d
WHERE  tc.fecha IS NULL
OPTION (MAXRECURSION 0);

DECLARE @min date = '2023-01-01',
        @max date = '2024-12-31';

;
WITH cte_fechas AS (
    SELECT @min AS d
    UNION ALL
    SELECT DATEADD(DAY,1,d) FROM cte_fechas WHERE d < @max
),
cte_join AS (
    SELECT f.d,
           tc.tipo_cambio_oficial,
           LAST_VALUE(tc.tipo_cambio_oficial) OVER (
               ORDER BY f.d
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS tipo_cambio_ffill
    FROM   cte_fechas f
    LEFT   JOIN ventas.DimTipoCambio tc
           ON tc.fecha = f.d
)
INSERT INTO ventas.DimTipoCambio (fecha, tipo_cambio_oficial)
SELECT d, tipo_cambio_ffill
FROM   cte_join
WHERE  tipo_cambio_oficial IS NULL     -- solo las fechas vacías
OPTION (MAXRECURSION 0);

SELECT COUNT(*) AS DiasTotales
FROM ventas.DimTipoCambio
WHERE fecha BETWEEN '2023-01-01' AND '2024-12-31';



/* 1. Asegurate de estar en la base correcta */
USE RetailAR;
GO

/* 2. Borra la vista si ya existe (por si la probaste antes) */
IF OBJECT_ID('ventas.vw_FactVentasEnriquecida', 'V') IS NOT NULL
    DROP VIEW ventas.vw_FactVentasEnriquecida;
GO

/* 3. Crea la vista definitiva */
CREATE VIEW ventas.vw_FactVentasEnriquecida AS
SELECT
      v.fecha_venta
    , v.id_sucursal
    , v.id_producto
    , v.cantidad
    , v.precio_unitario
    , v.canal_venta
    /* --- DimProducto --- */
    , pr.nombre_producto          AS nombre_producto
    , pr.categoria
    , pr.costo
    /* --- DimSucursal --- */
    , su.nombre_sucursal          AS nombre_sucursal
    , su.provincia
    , su.region
    /* --- DimTipoCambio --- */
    , tc.tipo_cambio_oficial
    /* --- DimLocalidad (coords) --- */
    , loc.latitud
    , loc.longitud
    /* --- Métricas de negocio --- */
    , v.cantidad * v.precio_unitario                         AS ImporteARS
    , v.cantidad * pr.costo                                  AS CostoTotalARS
    , v.cantidad * v.precio_unitario / tc.tipo_cambio_oficial AS ImporteUSD
    , (v.cantidad * v.precio_unitario) - (v.cantidad * pr.costo) AS MargenARS
FROM  ventas.FactVentas        AS v
JOIN  ventas.DimProducto       AS pr  ON v.id_producto  = pr.id_producto
JOIN  ventas.DimSucursal       AS su  ON v.id_sucursal  = su.id_sucursal
LEFT  JOIN ventas.DimTipoCambio AS tc ON v.fecha_venta = CAST(tc.fecha AS date)
LEFT  JOIN ventas.DimLocalidad  AS loc
          ON su.provincia       = loc.provincia_nombre






         AND su.nombre_sucursal = loc.ciudad;
GO
