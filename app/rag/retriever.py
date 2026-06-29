# RAG simplificado: contenido hardcodeado por business_id
# Próxima versión: migrar a Voyage AI embeddings para OOSS reales

BUSINESS_CONTENT = {
    "demo": """
RESTAURANTE: La Parrilla Don Carlos
TIPO: Parrilla argentina tradicional
DIRECCIÓN: Av. Corrientes 1847, Buenos Aires
TELÉFONO: (011) 4372-8890
HORARIOS:
- Lunes a viernes: 12:00 a 15:30 y 20:00 a 00:00
- Sábados: 12:00 a 16:00 y 20:00 a 01:00
- Domingos: 12:00 a 16:00 (cenas solo bajo reserva)

MENÚ - ENTRADAS:
- Provoleta a la parrilla: $4.500
- Chorizo criollo (x2): $3.800
- Morcilla artesanal (x2): $3.500
- Tabla de embutidos: $7.200
- Empanadas de carne (x3): $4.200

MENÚ - CARNES:
- Bife de chorizo (300g): $9.800
- Bife de chorizo (400g): $12.500
- Ojo de bife (300g): $11.200
- Entraña: $8.900
- Vacío: $8.200
- Asado de tira: $8.500
- Tira de asado completa (para 2): $16.800
- Pollo a la parrilla: $6.500
- Bondiola de cerdo: $7.800

MENÚ - GUARNICIONES (incluidas con las carnes principales):
- Papas fritas
- Papas al natural
- Ensalada mixta
- Puré de papas

MENÚ - PASTAS (viernes y sábados):
- Ñoquis con salsa: $5.200
- Tallarines a la bolognesa: $5.800
- Ravioles de ricota y espinaca: $6.200

MENÚ - POSTRES:
- Flan casero con crema y dulce de leche: $2.800
- Panqueques con dulce de leche: $3.200
- Helado artesanal (2 bochas): $2.500
- Brownie con helado: $3.800

BEBIDAS:
- Agua mineral (500ml): $1.200
- Gaseosas: $1.500
- Cerveza artesanal (500ml): $3.200
- Vino de la casa (copa): $2.800
- Vino Malbec Rutini (botella): $14.500
- Vino Torrontés (botella): $12.800

RESERVAS:
- Se aceptan reservas por teléfono o WhatsApp: +54 9 11 4372-8890
- Para grupos de más de 8 personas es obligatorio reservar con 24hs de anticipación
- Señas para eventos: 30% del consumo estimado

INFORMACIÓN ADICIONAL:
- Estacionamiento: hay playa de estacionamiento a media cuadra (Av. Corrientes 1820)
- Medios de pago: efectivo, tarjetas de débito y crédito, Mercado Pago (sin recargo)
- Menú del día (lunes a viernes al mediodía): entrada + plato principal + bebida por $8.500
- Se puede llevar perros pequeños al sector exterior
- Capacidad: 80 cubiertos en salón, 30 en terraza exterior
- WiFi disponible para clientes: red "DonCarlos_Wifi", clave: parrilla2024
""",
}

def search_documents(query: str, business_id: str, limit: int = 5) -> list:
    content = BUSINESS_CONTENT.get(business_id, BUSINESS_CONTENT.get("demo", ""))
    return [{"content": content}] if content else []

def ingest_text(text: str, business_id: str, metadata: dict = {}) -> None:
    # En esta versión simplificada el ingest es manual vía código
    # Próxima versión: Voyage AI embeddings + Supabase pgvector
    pass
