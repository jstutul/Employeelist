let registerData = {};
let skills = {};
let is_confirm = false;
let is_firstname = is_lastname = is_email = is_password = is_city = is_state = is_dob = is_skill = is_gender = is_phone = false;
var AddEmployeeForm = document.getElementById("addEmployeeForm");

// Add Employee Form Validation
    AddEmployeeForm.addEventListener("submit", function (event) {

        // Checking First Name
        alert("");
        if (registerData.firstname == "" || registerData.hasOwnProperty("firstname") == false) {
            printError("firstname", "Please enter your name");
        } else {
            var regex = /^[a-zA-Z\s]+$/;
            if (regex.test(registerData.firstname) === false) {
                is_firstname = false;
                printError("firstname", "Please enter a valid name");

            } else {
                is_firstname = true;
                printError("firstname", "");
            }
        }

        // Checking Last Name

        if (registerData.lastname == "" || registerData.hasOwnProperty("lastname") == false) {
            printError("lastname", "Please enter your name");
        } else {
            var regex = /^[a-zA-Z\s]+$/;
            if (regex.test(registerData.lastname) === false) {
                is_lastname = false;
                printError("lastname", "Please enter a valid name");

            } else {
                is_lastname = true;
                printError("lastname", "");

            }
        }

        // Checking Email
        if (registerData.email == "" || registerData.hasOwnProperty("email") == false) {
            printError("email", "Please enter your email");
        } else {
            var regex = /^\S+@\S+\.\S+$/;
            if (regex.test(registerData.email) === false) {
                is_email = false;
                printError("email", "Please enter a valid email");

            } else {
                is_email = true;
                printError("email", "");

            }
        }

       

        // Checking City Name
        if (registerData.city == "" || registerData.hasOwnProperty("city") == false) {
            printError("city", "Please select a city");
        } else {

            if (registerData.city === "Select") {
                is_city = false;
                printError("city", "Please select a city");

            } else {
                is_city = true;
                printError("city", "");
            }
        }

        // Checking Phone
        if (registerData.phone == "" || registerData.hasOwnProperty("phone") == false) {
            printError("phone", "Please enter your phone no");
        } else {
            var regex = /^\d{11}$/;;
            if (regex.test(registerData.phone) === false) {
                is_phone = false;
                printError("phone", "Phone no must be 11 digit");
            } else {
                is_phone = true;
                printError("phone", "");
            }
        }
        // Checking Date of Birth
        if (registerData.dob == "" || registerData.hasOwnProperty("dob") == false) {
            is_dob = false;
            printError("dob", "Please enter your date of birth");

        } else {
            is_dob = true;
            printError("dob", "");

        }

        // Checking Skills
        if (registerData.skills == "" || registerData.hasOwnProperty("skills") == false) {
            printError("skill", "Please select your all skills");
        } else {
            const check = Object.keys(registerData.skills).length;
            if (check === 0) {
                is_skill = false;
                printError("skill", "Select One Skill");
            }
            else {
                is_skill = true;
                printError("skill", "");

            }

        }
        //Checking Gender
        if (registerData.gender == "" || registerData.hasOwnProperty("gender") == false) {
            printError("gender", "Please select your gender");
        } else {
            if (registerData.skill === "Select") {
                is_gender = false;
                printError("gender", "Select your gender");

            } else {
                is_gender = true;
                printError("gender", "");

            }

        }
        console.log(is_lastname, is_firstname, is_email, is_city, is_phone, is_gender, is_skill);
        if (is_firstname === true && is_lastname === true && is_email === true && is_city === true && is_phone === true && is_gender === true && is_skill === true) {
            return true;
        }
        event.preventDefault();
        console.log(registerData);


    });



const handleOnBlur = (e) => {
    const field = e.target.name;
    const value = e.target.value;
    const NewData=registerData;
    NewData[field]=value;
    registerData = NewData;
    console.log(registerData);
}

const handleCheckbox = (e) => {
    const field = e.target;
    const value = e.target.value;
    const newData = skills;
    if (field.checked) {
        newData[field.id] = value;
        skills = newData;
    }
    else {

        delete skills[field.id];
    }

    const New = registerData;
    New["skills"] = skills;
    registerData = New;
    console.log(registerData);
}
function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
}

