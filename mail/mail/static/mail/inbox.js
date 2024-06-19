document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  //Get the data from input form
  document.querySelector('#compose-form').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function send_email(event) {

  event.preventDefault();
  //Select Input Data
  const recipientsData = document.querySelector("#compose-recipients").value;
  const subjectData = document.querySelector("#compose-subject").value;
  const bodyData = document.querySelector("#compose-body").value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipientsData,
        subject: subjectData,
        body: bodyData
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#details-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get all mailbox
  fetch(`/emails/${mailbox}`)
  //Put response into json form
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      emails.forEach(add_content)
    
  });

};

function add_content(contents) {

  //Creat new element
  const element = document.createElement('div');
  element.className = 'inboxEmail';
  element.innerHTML = `<div> <strong> ${contents.sender}</strong> ${contents.subject}</div>
                      <div> ${contents.timestamp}</div>`;

  //Check email whether it is read or not
  if (contents.read === true) {
      element.style.background = '#D3D3D3';
  } else {
    element.style.background = 'white';
  }

  // View email via click on an email
  element.addEventListener('click', () => {
    view_email(contents.id)
  });


  // Add content to DOM
  document.querySelector('#emails-view').append(element);

  //Create archive/unchive button
  const archiveBtn = document.createElement('button');
  archiveBtn.className = 'btn btn-sm btn-outline-primary archivebtn';
  archiveBtn.innerHTML = contents.archived ? "Unarchive" : "Archive";
  archiveBtn.addEventListener('click', () => {
    fetch(`/emails/${contents.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: !contents.archived
      })
    })
    .then(() => { load_mailbox('inbox')})

  });

  // Add archive button to DOM
  document.querySelector('#emails-view').append(archiveBtn);

  //Create Reply button
  const replyBtn = document.createElement('button');
  replyBtn.className = 'btn btn-sm btn-outline-primary replybtn';
  replyBtn.innerHTML = "Reply";
  replyBtn.addEventListener('click', () => {
    compose_email();

    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'block';

    // Fill composition fields
    document.querySelector('#compose-recipients').value = `${contents.sender}`;
    const subject = contents.subject;
    if (subject.split(" ", 1) != "Re:") {
      document.querySelector('#compose-subject').value = `Re: ${contents.subject}`
    }
    document.querySelector('#compose-body').value = `"On ${contents.timestamp} ${contents.sender} wrote: ${contents.body}"`;

  });

  // Add reply button to DOM
  document.querySelector('#emails-view').append(replyBtn);

};

function view_email(id) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // Show the details-email-view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';

      const element = document.querySelector('#details-email-view');
      element.style.display = 'block';
      element.innerHTML= `<div><strong>From:</strong> ${email.sender}</div>
      <div><strong>To:</strong> ${email.recipients}</div>
      <div><strong>Subject:</strong> ${email.subject}</div>
      <div><strong>Timestamp:</strong> ${email.timestamp}</div>
      <div class="emailBody">${email.body}</div>`;

      // Change read value to true
      if (email.read === false) {
        fetch(`/emails/${email.id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }


      //Create Reply button
      const replyBtn = document.createElement('button');
      replyBtn.className = 'btn btn-sm btn-outline-primary replybtn';
      replyBtn.innerHTML = "Reply";
      replyBtn.addEventListener('click', () => {
      compose_email();

      // Show compose view and hide other views
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'block';
      document.querySelector('#details-email-view').style.display = 'none';

      // Fill composition fields
      document.querySelector('#compose-recipients').value = `${email.sender}`;
      let subject = email.subject;
      if (subject.split(" ", 1)[0] != "Re:") {
        document.querySelector('#compose-subject').value = "Re: "  + email.subject;
      } else {
        document.querySelector('#compose-subject').value = subject;
      }
        
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;

      });

      // Add reply button to DOM
      document.querySelector('#details-email-view').append(replyBtn);

  });
}
