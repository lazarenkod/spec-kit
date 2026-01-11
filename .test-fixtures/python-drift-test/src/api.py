"""
Product Catalog API
FastAPI implementation with intentional drift scenarios
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Product Catalog API")


class ProductData(BaseModel):
    """Product creation/update data"""
    name: str = Field(..., min_length=1)
    description: str = ""
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


class Product(BaseModel):
    """Product model"""
    id: str
    name: str
    description: str
    price: float
    stock: int
    created_at: datetime
    is_active: bool = True


# @speckit:FR:FR-001
@app.post("/api/products", status_code=status.HTTP_201_CREATED)
async def create_product(data: ProductData) -> Product:
    """
    Create a new product

    Validates:
    - Name is non-empty (handled by Pydantic)
    - Price is positive (handled by Pydantic Field)
    - Stock is non-negative (handled by Pydantic Field)
    """
    product = Product(
        id=generate_id(),
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        created_at=datetime.now(),
        is_active=True
    )

    # Save to database (mock)
    await save_product(product)

    return product


# @speckit:FR:FR-003
@app.patch("/api/products/{product_id}")
async def update_product(product_id: str, updates: ProductData) -> Product:
    """
    Update product information

    NOTE: This implementation only updates price, NOT stock
    This is BEHAVIORAL DRIFT - spec says it should update all fields
    """
    product = await get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # DRIFT: Only updating price, ignoring stock and other fields
    if updates.price:
        old_price = product.price
        product.price = updates.price

        # Audit log as required by spec
        await create_audit_log(product_id, "price_change", old_price, updates.price)

    # MISSING: Should also update stock, name, description

    await save_product(product)
    return product


# @speckit:FR:FR-004
@app.delete("/api/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str) -> None:
    """
    Soft-delete a product

    Marks product as inactive rather than removing from database
    """
    product = await get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check for active orders
    if await has_active_orders(product_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot delete product with active orders"
        )

    # Soft delete
    product.is_active = False
    await save_product(product)


@app.get("/api/products/{product_id}/inventory")
async def get_product_inventory(product_id: str) -> dict:
    """
    Get detailed inventory information for a product

    NOTE: This endpoint is NOT in spec.md (reverse drift scenario)
    It's implemented but not documented in requirements
    """
    product = await get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Additional inventory details not in spec
    return {
        "product_id": product_id,
        "current_stock": product.stock,
        "reserved": await get_reserved_stock(product_id),
        "available": product.stock - await get_reserved_stock(product_id),
        "reorder_point": 5,  # Business logic not in spec
        "last_restocked": datetime.now()  # Tracking not in spec
    }


@app.post("/api/products/bulk-import")
async def bulk_import_products(products: List[ProductData]) -> dict:
    """
    Bulk import products from external system

    NOTE: This endpoint is also NOT in spec.md (reverse drift scenario)
    Internal tool that evolved into a public API
    """
    imported = []
    failed = []

    for product_data in products:
        try:
            product = await create_product(product_data)
            imported.append(product.id)
        except Exception as e:
            failed.append({"data": product_data.dict(), "error": str(e)})

    return {
        "imported_count": len(imported),
        "failed_count": len(failed),
        "imported_ids": imported,
        "failures": failed
    }


# @internal
async def archive_discontinued_products(days_inactive: int = 90) -> int:
    """
    Archive products that have been inactive for specified days

    This is an internal maintenance function - should be ignored by drift detection
    """
    products = await find_inactive_products(days_inactive)

    for product in products:
        await archive_product(product.id)

    return len(products)


# Helper functions (mock implementations)
def generate_id() -> str:
    """Generate unique product ID"""
    import uuid
    return str(uuid.uuid4())


async def save_product(product: Product) -> None:
    """Save product to database (mock)"""
    print(f"Saving product: {product.id}")


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Retrieve product by ID (mock)"""
    # Mock implementation returns dummy product
    return Product(
        id=product_id,
        name="Test Product",
        description="Test Description",
        price=99.99,
        stock=10,
        created_at=datetime.now(),
        is_active=True
    )


async def create_audit_log(product_id: str, action: str, old_value: any, new_value: any) -> None:
    """Create audit log entry (mock)"""
    print(f"Audit log: {product_id} - {action}: {old_value} -> {new_value}")


async def has_active_orders(product_id: str) -> bool:
    """Check if product has active orders (mock)"""
    return False


async def get_reserved_stock(product_id: str) -> int:
    """Get reserved stock count (mock)"""
    return 0


async def find_inactive_products(days_inactive: int) -> List[Product]:
    """Find products inactive for specified days (mock)"""
    return []


async def archive_product(product_id: str) -> None:
    """Archive product (mock)"""
    print(f"Archiving product: {product_id}")
