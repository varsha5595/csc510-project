import unittest
from unittest.mock import patch
import http.client

from src.sync_ends_service import get_postman_collections
from src.sync_ends_service import get_selected_collection
from src.sync_ends_service import regex