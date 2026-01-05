function initBooking() {
  const selectedDateInput = document.getElementById("selected_date");
  const timeSlotContainer = document.getElementById("time_slot_container");
  const timeSlotsGrid = document.getElementById("time_slots_grid");
  const slotsLoading = document.getElementById("slots_loading");
  const bookingDateHidden = document.getElementById("booking_date");
  const bookingForm = document.getElementById("bookingForm");

  let selectedSlot = null;

  if (selectedDateInput && bookingForm) {
    const serviceIdInput = document.querySelector('input[name="service_id"]');
    const serviceId = serviceIdInput ? serviceIdInput.value : null;

    selectedDateInput.addEventListener("change", async function () {
      const selectedDate = this.value;

      if (!selectedDate || !serviceId) {
        return;
      }

      timeSlotContainer.style.display = "block";
      slotsLoading.style.display = "block";
      timeSlotsGrid.innerHTML = "";
      selectedSlot = null;
      bookingDateHidden.value = "";

      try {
        const response = await fetch("/booking/check_availability", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            jsonrpc: "2.0",
            method: "call",
            params: {
              service_id: parseInt(serviceId),
              date: selectedDate,
            },
          }),
        });

        const data = await response.json();

        slotsLoading.style.display = "none";

        if (data.error) {
          timeSlotsGrid.innerHTML =
            '<div class="alert alert-danger">Error loading availability. Please try again.</div>';
          return;
        }

        const result = data.result;

        if (result.error) {
          timeSlotsGrid.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
          return;
        }

        renderTimeSlots(result.slots);
      } catch (error) {
        slotsLoading.style.display = "none";
        timeSlotsGrid.innerHTML =
          '<div class="alert alert-danger">Failed to load time slots. Please refresh and try again.</div>';
      }
    });

    function renderTimeSlots(slots) {
      if (!slots || slots.length === 0) {
        timeSlotsGrid.innerHTML =
          '<div class="alert alert-warning">No time slots available for this date.</div>';
        return;
      }

      timeSlotsGrid.innerHTML = "";

      slots.forEach((slot) => {
        const slotDiv = document.createElement("div");
        slotDiv.className = "time-slot";

        if (slot.is_past) {
          slotDiv.classList.add("past", "disabled");
        } else if (slot.is_full) {
          slotDiv.classList.add("full", "disabled");
        } else if (slot.available) {
          slotDiv.classList.add("available");
        }

        const slotTime = document.createElement("span");
        slotTime.className = "slot-time";
        slotTime.textContent = slot.display;

        const slotCapacity = document.createElement("span");
        slotCapacity.className = "slot-capacity";

        if (slot.is_past) {
          slotCapacity.textContent = "Past";
        } else if (slot.is_full) {
          slotCapacity.textContent = `Full (${slot.current_bookings}/${slot.max_capacity})`;
        } else if (slot.available) {
          if (slot.max_capacity === 0) {
            slotCapacity.textContent = "Unlimited";
          } else {
            const remaining = slot.max_capacity - slot.current_bookings;
            slotCapacity.textContent = `${remaining} left`;
          }
        }

        slotDiv.appendChild(slotTime);
        slotDiv.appendChild(slotCapacity);

        if (slot.available) {
          slotDiv.addEventListener("click", function () {
            selectTimeSlot(this, slot.datetime);
          });
        }

        timeSlotsGrid.appendChild(slotDiv);
      });
    }

    function selectTimeSlot(slotElement, datetime) {
      const previousSelected = timeSlotsGrid.querySelector(
        ".time-slot.selected"
      );
      if (previousSelected) {
        previousSelected.classList.remove("selected");
        previousSelected.classList.add("available");
      }

      slotElement.classList.remove("available");
      slotElement.classList.add("selected");

      bookingDateHidden.value = datetime;
      selectedSlot = datetime;

      const notesSection = document.querySelector('textarea[name="notes"]');
      if (notesSection) {
        setTimeout(() => {
          notesSection.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);
      }
    }

    if (bookingForm) {
      const phoneInput = document.getElementById("customer_phone");
      if (phoneInput) {
        phoneInput.addEventListener("input", function (e) {
          let value = e.target.value.replace(/\D/g, "");
          e.target.value = value;
        });

        phoneInput.addEventListener("change", function () {
          this.setCustomValidity("");
        });
      }

      const useAccountInfoToggle = document.getElementById("useAccountInfo");
      if (useAccountInfoToggle) {
        const customerFields = document.querySelectorAll(".customer-field");
        const originalValues = {};

        customerFields.forEach((field) => {
          originalValues[field.id] = field.value;
        });

        useAccountInfoToggle.addEventListener("change", function () {
          if (this.checked) {
            customerFields.forEach((field) => {
              field.value = originalValues[field.id];
              field.readOnly = true;
              field.classList.add("bg-light");
            });
          } else {
            customerFields.forEach((field) => {
              field.readOnly = false;
              field.classList.remove("bg-light");
            });
          }
        });

        if (useAccountInfoToggle.checked) {
          customerFields.forEach((field) => {
            field.readOnly = true;
            field.classList.add("bg-light");
          });
        }
      }

      bookingForm.addEventListener("submit", function (e) {
        const submitBtn = bookingForm.querySelector('button[type="submit"]');
        const countryCodeSelect = document.getElementById("country_code");
        const phoneInput = document.getElementById("customer_phone");

        if (selectedDateInput && !bookingDateHidden.value) {
          e.preventDefault();
          alert("Please select a time slot before submitting.");
          timeSlotContainer.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
          return;
        }

        if (countryCodeSelect && phoneInput && phoneInput.value) {
          const countryCode = countryCodeSelect.value;
          const phoneNumber = phoneInput.value.trim();

          const existingHidden = bookingForm.querySelector(
            'input[name="customer_phone"][type="hidden"]'
          );
          if (existingHidden) {
            existingHidden.remove();
          }

          const fullPhoneInput = document.createElement("input");
          fullPhoneInput.type = "hidden";
          fullPhoneInput.name = "customer_phone";
          fullPhoneInput.value = countryCode + " " + phoneNumber;

          phoneInput.disabled = true;
          bookingForm.appendChild(fullPhoneInput);
        }

        if (submitBtn) {
          submitBtn.classList.add("loading");
          submitBtn.disabled = true;
          submitBtn.innerHTML =
            '<i class="fa fa-spinner fa-spin me-2"></i>Processing...';
        }
      });
    }

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener("click", function (e) {
        const href = this.getAttribute("href");
        if (href !== "#") {
          e.preventDefault();
          const target = document.querySelector(href);
          if (target) {
            target.scrollIntoView({
              behavior: "smooth",
              block: "start",
            });
          }
        }
      });
    });

    const observerOptions = {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    };

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "0";
          entry.target.style.transform = "translateY(20px)";

          setTimeout(() => {
            entry.target.style.transition = "all 0.6s ease";
            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";
          }, 100);

          observer.unobserve(entry.target);
        }
      });
    }, observerOptions);

    document.querySelectorAll(".service-card").forEach((card) => {
      observer.observe(card);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initBooking);
  } else {
    initBooking();
  }
}
