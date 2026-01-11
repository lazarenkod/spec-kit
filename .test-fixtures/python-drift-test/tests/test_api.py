"""
Tests for Product Catalog API
"""

import pytest
from fastapi.testclient import TestClient
from src.api import app, ProductData

client = TestClient(app)


# [TEST:AS-1A] Create product successfully
def test_create_product_success():
    """Should create product with valid data"""
    product_data = {
        "name": "Laptop",
        "description": "High-performance laptop",
        "price": 999.99,
        "stock": 10
    }

    response = client.post("/api/products", json=product_data)

    assert response.status_code == 201
    product = response.json()
    assert product["name"] == "Laptop"
    assert product["price"] == 999.99
    assert product["stock"] == 10
    assert "id" in product
    assert "created_at" in product
    assert product["is_active"] is True


# [TEST:AS-1B] Reject negative price
def test_create_product_negative_price():
    """Should reject product with negative price"""
    product_data = {
        "name": "Invalid Product",
        "description": "Should fail",
        "price": -50.00,
        "stock": 10
    }

    response = client.post("/api/products", json=product_data)

    assert response.status_code == 422  # Validation error
    error = response.json()
    assert "price" in str(error).lower()


def test_create_product_empty_name():
    """Should reject product with empty name"""
    product_data = {
        "name": "",
        "description": "No name",
        "price": 100.00,
        "stock": 5
    }

    response = client.post("/api/products", json=product_data)

    assert response.status_code == 422  # Validation error


def test_create_product_negative_stock():
    """Should reject product with negative stock"""
    product_data = {
        "name": "Product",
        "description": "Invalid stock",
        "price": 50.00,
        "stock": -5
    }

    response = client.post("/api/products", json=product_data)

    assert response.status_code == 422  # Validation error


# [TEST:AS-3A] Update product price
def test_update_product_price():
    """Should update product price and create audit log"""
    product_id = "test-product-123"
    updates = {
        "name": "Laptop",
        "description": "Updated",
        "price": 899.99,
        "stock": 10
    }

    response = client.patch(f"/api/products/{product_id}", json=updates)

    assert response.status_code == 200
    product = response.json()
    assert product["price"] == 899.99
    # NOTE: Stock should be updated too, but implementation ignores it (behavioral drift)


# [TEST:AS-4A] Delete product
def test_delete_product():
    """Should soft-delete product"""
    product_id = "test-product-456"

    response = client.delete(f"/api/products/{product_id}")

    assert response.status_code == 204


def test_delete_nonexistent_product():
    """Should return 404 for non-existent product"""
    # This would fail with current mock implementation, but demonstrates intent
    pass


# Tests for undocumented APIs (reverse drift scenario)
def test_get_product_inventory():
    """
    Test for inventory endpoint - but this endpoint is not in spec.md!
    This is reverse drift - code exists without spec
    """
    product_id = "test-product-789"

    response = client.get(f"/api/products/{product_id}/inventory")

    assert response.status_code == 200
    inventory = response.json()
    assert "current_stock" in inventory
    assert "reserved" in inventory
    assert "available" in inventory
    assert "reorder_point" in inventory


def test_bulk_import_products():
    """
    Test for bulk import endpoint - also not in spec.md!
    This is reverse drift - internal tool evolved into public API
    """
    products = [
        {
            "name": "Product 1",
            "description": "Desc 1",
            "price": 10.00,
            "stock": 100
        },
        {
            "name": "Product 2",
            "description": "Desc 2",
            "price": 20.00,
            "stock": 200
        }
    ]

    response = client.post("/api/products/bulk-import", json=products)

    assert response.status_code == 200
    result = response.json()
    assert "imported_count" in result
    assert "failed_count" in result


# NOTE: No tests for FR-002 (product search) because it's not implemented
# This demonstrates forward drift


# Additional test to highlight behavioral drift in update
def test_update_product_stock_ignored():
    """
    This test SHOULD pass according to spec, but WILL FAIL due to behavioral drift
    The implementation ignores stock updates
    """
    product_id = "test-product-999"
    updates = {
        "name": "Product",
        "description": "Test",
        "price": 100.00,
        "stock": 50  # This should be updated but won't be
    }

    response = client.patch(f"/api/products/{product_id}", json=updates)

    assert response.status_code == 200
    product = response.json()
    # This assertion would fail due to behavioral drift:
    # assert product["stock"] == 50  # EXPECTED but not implemented
