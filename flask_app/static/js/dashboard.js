document.addEventListener("DOMContentLoaded", () => {

  const csrfToken = document.querySelector(
    'input[name="csrf_token"]'
  ).value;

  const dropdownOptions = {
    client_contact: [
      { value: "awaiting", label: "Awaiting" },
      { value: "scheduled", label: "Scheduled" },
      { value: "visited", label: "Visited" },
      { value: "no_contact", label: "No Contact" },
      { value: "cancelled", label: "Cancelled" }
    ],

    client_gender: [
      { value: "male", label: "Male" },
      { value: "female", label: "Female" }
    ],

    resident_type: [
      { value: "private resident", label: "Private Resident" },
      { value: "supported independent living", label: "Supported Independent Living" },
      { value: "group home", label: "Group Home" },
      { value: "aged care", label: "Aged Care" },
      { value: "other", label: "Other" }
    ],

    referral_type: [
      { value: "support at home", label: "Support at Home" },
      { value: "ndis", label: "NDIS" },
      { value: "wc ctp", label: "WC / CTP" },
      { value: "chronic condition", label: "Chronic Condition Management Plan" },
      { value: "private health insurance", label: "Private Health Insurance" },
      { value: "not sure", label: "Not Sure" }
    ],

    relationship_to_client: [
      { value: "client", label: "Client" },
      { value: "general practitioner", label: "General Practitioner" },
      {
        value: "family member / support coordinator / case manager / carer",
        label: "Family Member / Support Coordinator / Case Manager / Carer"
      }
    ]
  };

  function createInput(cell) {
    const field = cell.dataset.field;
    const value = cell.dataset.value ?? "";

    // Handle all database-constrained dropdown fields.
    if (dropdownOptions[field]) {
      const select = document.createElement("select");

      const placeholder = document.createElement("option");
      placeholder.value = "";
      placeholder.textContent = "Please select an option";
      placeholder.disabled = true;
      placeholder.hidden = true;
      select.appendChild(placeholder);

      dropdownOptions[field].forEach(({ value: optionValue, label }) => {
        const option = document.createElement("option");
        option.value = optionValue;
        option.textContent = label;
        option.selected = optionValue === value;
        select.appendChild(option);
      });

      if (!dropdownOptions[field].some(option => option.value === value)) {
        placeholder.selected = true;
      }

      return select;
    }

    // Handle textareas.
    if (cell.dataset.type === "textarea") {
      const textarea = document.createElement("textarea");
      textarea.value = value;
      return textarea;
    }

    // Handle remaining text/date fields.
    const input = document.createElement("input");
    input.type = field === "client_dob" ? "date" : "text";
    input.value = value;

    return input;
  }

  function enableEditing(row) {
    const cells = row.querySelectorAll("[data-field]");

    cells.forEach(cell => {
      const input = createInput(cell);
      cell.replaceChildren(input);
    });

    const actions = row.querySelector(".actions");

    actions.innerHTML = `
            <button type="button" class="btn-save">Save</button>
            <button type="button" class="btn-cancel">Cancel</button>
        `;
  }

  function cancelEditing(row) {
    row.querySelectorAll("[data-field]").forEach(cell => {
      cell.textContent = cell.dataset.display;
    });

    restoreButtons(row);
  }

  function restoreButtons(row) {
    const actions = row.querySelector(".actions");

    actions.innerHTML = `
            <button type="button" class="btn-edit">Edit</button>
            <button type="button" class="btn-delete">Delete</button>
        `;
  }

  async function saveBooking(row) {
    const bookingId = row.dataset.bookingId;
    const cells = row.querySelectorAll("[data-field]");

    const data = {};

    cells.forEach(cell => {
      const input = cell.querySelector("input, textarea, select");
      data[cell.dataset.field] = input.value;
    });

    try {
      const response = await fetch(`/admin/bookings/${bookingId}`, {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        const result = await response.json().catch(() => ({}));
        alert(result.error || "Failed to update booking.");
        return;
      }

      // Reload to display the updated database values.
      window.location.reload();

    } catch (error) {
      console.error("Booking update failed:", error);
      alert("An error occurred while updating the booking.");
    }
  }

  document.addEventListener("click", event => {
    const button = event.target.closest("button");
    if (!button) return;

    const row = button.closest("tr[data-booking-id]");
    if (!row) return;

    if (button.classList.contains("btn-edit")) {
      enableEditing(row);
    }

    if (button.classList.contains("btn-cancel")) {
      cancelEditing(row);
    }

    if (button.classList.contains("btn-save")) {
      saveBooking(row);
    }
  });

});