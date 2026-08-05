document.addEventListener("DOMContentLoaded", () => {
  //ELEMENTS
  const unitSearch = document.getElementById("unitSearch");
  const searchResults = document.getElementById("unitSearchResults");
  const selectedUnitCard = document.getElementById("selectedUnitCard");
  const unitIdInput = document.getElementById("unitId");
  const clearSelectedUnit = document.getElementById("clearSelectedUnit");
  const deploymentForm = document.getElementById("deploymentForm");
  // CHECK REQUIRED ELEMENTS
  if (
    !unitSearch ||
    !searchResults
  ) {
    console.error(
      "Deployment search elements were not found."
    );
    return;
  }
  //SEARCH TIMER
  let searchTimer;
  //SEARCH AVAILABLE UNITS
  unitSearch.addEventListener(
    "input",
    () => {
      clearTimeout(
        searchTimer
      );
      const searchValue =
        unitSearch.value.trim();
      //HIDE RESULTS WHEN INPUT IS EMPTY
      if (
        searchValue.length === 0
      ) {
        searchResults.innerHTML =
          "";
        searchResults.hidden =
          true;
        return;
      }
      // WAIT FOR AT LEAST 2 CHARACTERS
      if (
        searchValue.length < 2
      ) {
        searchResults.innerHTML = `
          <div class="search-message">
            Type at least 2 characters...
          </div>
        `;
        searchResults.hidden =
          false;
        return;
      }
      //DELAY SEARCH
      searchTimer =
        setTimeout(
          () => {
            searchUnits(
              searchValue
            );
          },
          300
        );
    }
  );
  // FETCH AVAILABLE UNITS
  async function searchUnits(
    searchValue
  ) {
    searchResults.hidden =
      false;
    searchResults.innerHTML = `
      <div class="search-message">
        <i
          class="fa-solid fa-spinner fa-spin"
        ></i>
        Searching available units...
      </div>
    `;
    try {
      const response =
        await fetch(
          `/deployment/search-units?search=${encodeURIComponent(
            searchValue
          )}`
        );
      if (
        !response.ok
      ) {
        throw new Error(
          "Search request failed."
        );
      }
      const data =
        await response.json();
      //CLEAR OLD RESULTS
      searchResults.innerHTML =
        "";
      //NO RESULTS
      if (
        !data.units ||
        data.units.length === 0
      ) {
        searchResults.innerHTML = `
          <div class="search-message">
            <i
              class="fa-solid fa-circle-info"
            ></i>
            No available units found.
          </div>
        `;
        return;
      }
      // DISPLAY RESULTS
      data.units.forEach(
        (unit) => {
          const resultButton =
            document.createElement(
              "button"
            );
          resultButton.type =
            "button";
          resultButton.className =
            "unit-search-item";
          resultButton.innerHTML = `
            <div class="unit-search-icon">
              <i
                class="fa-solid fa-print"
              ></i>
            </div>
            <div class="unit-search-information">
              <strong>
                ${
                  unit.asset_code ||
                  "No Asset Code"
                }
              </strong>
              <span>
                ${
                  unit.brand ||
                  ""
                }
                ${
                  unit.model ||
                  ""
                }
              </span>
              <small>
                ${
                  unit.unit_category ||
                  "Unit"
                }
              </small>
            </div>
            <span class="unit-search-status">
              Available
            </span>
          `;
          //SELECT UNIT
          resultButton.addEventListener(
            "click",
            () => {
              selectUnit(
                unit
              );
            }
          );
          searchResults.appendChild(
            resultButton
          );
        }
      );
      searchResults.hidden =
        false;
    } catch (
      error
    ) {
      console.error(
        "Unit search error:",
        error
      );
      searchResults.innerHTML = `
        <div class="search-message error">
          <i
            class="fa-solid fa-triangle-exclamation"
          ></i>
          Unable to search units.
        </div>
      `;
      searchResults.hidden =
        false;
    }
  }
  // SELECT UNIT
  function selectUnit(
    unit
  ) {
    //SAVE UNIT ID
    unitIdInput.value =
      unit.id;
    //DISPLAY UNIT INFORMATION
    document.getElementById(
      "selectedAssetCode"
    ).textContent =
      unit.asset_code ||
      "-";
    document.getElementById(
      "selectedBrand"
    ).textContent =
      unit.brand ||
      "-";
    document.getElementById(
      "selectedModel"
    ).textContent =
      unit.model ||
      "-";
    document.getElementById(
      "selectedSerialNumber"
    ).textContent =
      unit.serial_number ||
      "-";
    document.getElementById(
      "selectedAvailability"
    ).textContent =
      unit.status ||
      "Available";
    // SHOW SELECTED UNIT
    selectedUnitCard.hidden =
      false;
    // CLEAR SEARCH
    unitSearch.value =
      "";
    searchResults.innerHTML =
      "";
    searchResults.hidden =
      true;
    // SCROLL TO SELECTED UNIT
    selectedUnitCard.scrollIntoView({
      behavior:
        "smooth",
      block:
        "nearest"
    });
  }
  // REMOVE SELECTED UNIT
  if (
    clearSelectedUnit
  ) {
    clearSelectedUnit.addEventListener(
      "click",
      () => {
        unitIdInput.value =
          "";
        selectedUnitCard.hidden =
          true;
        unitSearch.value =
          "";
        unitSearch.focus();
      }
    );
  }
  // FORM VALIDATION
  if (
    deploymentForm
  ) {
    deploymentForm.addEventListener(
      "submit",
      (event) => {
        if (
          !unitIdInput.value
        ) {
          event.preventDefault();
          alert(
            "Please search and select an available unit first."
          );
          unitSearch.focus();
        }
      }
    );
  }
});
