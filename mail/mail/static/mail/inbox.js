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
      emails.forEach(email => add_content(email, mailbox))
  });
};

function add_content(contents, mailbox) {

  //Creat new element
  const element = document.createElement('div');
  element.className = 'inboxEmail';
  element.innerHTML = `<div class="mar"> <strong> ${contents.sender}</strong> ${contents.subject}</div>
                      <div class="mar"> ${contents.timestamp}</div>`;

  //Check email whether it is read or not
  if (contents.read === true) {
      element.style.background = '#cfcfcf';
  } else {
    element.style.background = 'white';
  }

  // Create archive/unarchive button if mailbox is not 'sent'
  if (mailbox !== 'sent') {
    const archiveBtn = document.createElement('button');
    archiveBtn.className = 'btn btn-sm btn-outline-primary mx-2';
    archiveBtn.innerHTML = contents.archived ? "Unarchive" : "Archive";
    archiveBtn.addEventListener('click', (event) => {
      event.stopPropagation(); // Prevent parent click event
      fetch(`/emails/${contents.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !contents.archived
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(() => { load_mailbox('inbox') });
    });

    // Append the archive button to the email element
    element.appendChild(archiveBtn);

  }

  // View email via click on an email
  element.addEventListener('click', () => {
    view_email(contents.id)
  });

  //Create Reply button
  const replyBtn = document.createElement('button');
  replyBtn.className = 'btn btn-sm btn-outline-primary mx-2';
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
  element.appendChild(replyBtn);

  // Add content to DOM
  document.querySelector('#emails-view').append(element);

  
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
