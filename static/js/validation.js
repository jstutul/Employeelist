let registerData = {};
let skills = {};
let is_confirm = false;
let is_firstname = is_lastname = is_email = is_password = is_city = is_state = is_dob = is_skill = is_gender = is_phone = false;
let AddEmployeeForm = document.getElementById("addEmployeeForm");
let editEmployeeForm = document.getElementById("editEmployeeForm");

if(editEmployeeForm){
    Action(editEmployeeForm);
}
if(AddEmployeeForm){
    Action(AddEmployeeForm);
}

function Action(form){

    form.addEventListener("submit", function (event) {
        let isValid=0;
        let firstname=document.getElementById("FormFirstName").value;
        let lastname=document.getElementById("FormLastName").value;
        let email=document.getElementById("FormEmail").value;
        let city=document.getElementById("FormCity").value;
        let phone=document.getElementById("FormPhone").value;
        let dob=document.getElementById("FormDob").value;
        let gender1=document.getElementById("inlineRadio1");
        let gender2=document.getElementById("inlineRadio2");
        let skills = document.getElementById("skillsZone");
        var chks = document.querySelectorAll('input[type="checkbox"]')

        // Checking First Name
        if (firstname == "" || firstname==null) {
            isValid++;
            printError("firstname", "Please enter your name");
        } else {
            var regex = /^[a-zA-Z\s]+$/;
            if (regex.test(firstname) === false) {
                is_firstname = false;
                isValid++;
                printError("firstname", "Please enter a valid name");
            } else {
                is_firstname = true;
                printError("firstname", "");
            }
        }

        // Checking Last Name

        if (lastname == "" || lastname == null) {
            printError("lastname", "Please enter your name");
            isValid++;
        } else {
            var regex = /^[a-zA-Z\s]+$/;
            if (regex.test(lastname) === false) {
                is_lastname = false;
                isValid++;
                printError("lastname", "Please enter a valid name");

            } else {
                is_lastname = true;
                printError("lastname", "");

            }
        }

        // Checking Email
        if (email == "" || email == null) {
            isValid++;
            printError("email", "Please enter your email");
        } else {
            var regex = /^\S+@\S+\.\S+$/;
            if (regex.test(email) === false) {
                is_email = false;
                isValid++;
                printError("email", "Please enter a valid email");

            } else {
                is_email = true;
                printError("email", "");

            }
        }

       

        // Checking City Name
        if (city == "" || city == null) {
            isValid++;
            printError("city", "Please select a city");
        } else {

            if (city === "Select") {
                is_city = false;
                isValid++;
                printError("city", "Please select a city");

            } else {
                is_city = true;
                printError("city", "");
            }
        }

        // Checking Phone
        if (phone == "" || phone == null) {
            isValid++;
            printError("phone", "Please enter your phone no");
        } else {
            var regex = /^\d{11}$/;;
            if (regex.test(phone) === false) {
                is_phone = false;
                isValid++;
                printError("phone", "Phone no must be 11 digit");
            } else {
                is_phone = true;
                printError("phone", "");
            }
        }
        // Checking Date of Birth
        if (dob == "" || dob == null) {
            is_dob = false;
            isValid++;
            printError("dob", "Please select your date of birth");

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
                isValid++;
                printError("skill", "Select One Skill");
            }
            else {
                is_skill = true;
                printError("skill", "");

            }

        }
        //Checking Gender
        if (gender1.checked ==false  && gender2.checked  == false) {
            isValid++;
            printError("gender", "Please select your gender");
        } else {
            is_gender = true;
            printError("gender", "");
        }
        let skill_error=0;
        for (i = 0; i < chks.length; i += 1) {
           
            if (chks[i].checked == true){
                printError("skill", "");
            }
            else{
                skill_error++;
                printError("skill", "Select al least one Skill");
            }
        }
        if(skill_error>=5){
            isValid++;
        }
       
        console.log(isValid);
        if (isValid==0) {
            return true;
        }

        event.preventDefault();
    });
}

function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
}

