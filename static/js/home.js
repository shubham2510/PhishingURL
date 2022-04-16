function validate() {
    var x = document.forms["searchForm"]["search"].value;
    if (x == "") {
        alert("Search Something...");
        return false;
    }
}

function regvalidate(){
  var email = document.forms["registerForm"]["txtEmail"].value;
  var phone = document.forms["registerForm"]["txtMobile"].value;
  var pass1 = document.forms["registerForm"]["password1"].value;
  var pass2 = document.forms["registerForm"]["password2"].value;
  var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
  if (reg.test(email) == false)
  {
      alert('Invalid Email Address');
      return false;
  }

  else if((phone.length !=10){
    alert("Please Enter Valid 10 digit Phone Number");
    return false;
  }


  else if (pass1 != pass2) {
      alert("Password Does not Match");
      return false;
  }
}
