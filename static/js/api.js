/**
 * FindIt - Centralized API Service for Flask Backend Integration
 * All fetch helper functions correspond to your teammate's Flask route endpoints.
 */

const API_BASE_URL = "/api";

const ApiService = {
  /**
   * Register a new user
   * Payload: { full_name, email, password, phone_number }
   */
  async registerUser(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
      });
      return await response.json();
    } catch (error) {
      console.error("Error registering user:", error);
      throw error;
    }
  },

  /**
   * Log in user
   * Payload: { email, password }
   */
  async loginUser(credentials) {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credentials)
      });
      return await response.json();
    } catch (error) {
      console.error("Error logging in:", error);
      throw error;
    }
  },

  /**
   * Report an item (Supports FormData for image uploads)
   * Form Fields: item_name, item_description, category, item_type, location, date_lost_found, image
   */
  async reportItem(formData) {
    try {
      const response = await fetch(`${API_BASE_URL}/items`, {
        method: "POST",
        body: formData // Note: Content-Type header is left unset so browser sets multipart boundary
      });
      return await response.json();
    } catch (error) {
      console.error("Error reporting item:", error);
      throw error;
    }
  },

  /**
   * Fetch list of items with optional query filters (category, item_type, query)
   */
  async getItems(filters = {}) {
    try {
      const params = new URLSearchParams(filters).toString();
      const response = await fetch(`${API_BASE_URL}/items?${params}`);
      return await response.json();
    } catch (error) {
      console.error("Error fetching items:", error);
      throw error;
    }
  },

  /**
   * Fetch single item by ID
   */
  async getItemById(itemId) {
    try {
      const response = await fetch(`${API_BASE_URL}/items/${itemId}`);
      return await response.json();
    } catch (error) {
      console.error(`Error fetching item ${itemId}:`, error);
      throw error;
    }
  },

  /**
   * Submit a claim for an item
   * Payload: { claim_message }
   */
  async submitClaim(itemId, claimData) {
    try {
      const response = await fetch(`${API_BASE_URL}/items/${itemId}/claim`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(claimData)
      });
      return await response.json();
    } catch (error) {
      console.error(`Error submitting claim for item ${itemId}:`, error);
      throw error;
    }
  },

  /**
   * Fetch current user's submitted claims
   */
  async getMyClaims() {
    try {
      const response = await fetch(`${API_BASE_URL}/my-claims`);
      return await response.json();
    } catch (error) {
      console.error("Error fetching claims:", error);
      throw error;
    }
  }
};
