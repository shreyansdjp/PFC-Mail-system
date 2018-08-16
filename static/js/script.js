

$('#addEmail').click(function(event) {
    $('#email_field').append(`<input type="text" class="form-control mt-2" name="email" id="emails" placeholder="Email" autofocus autocomplete="off" required>`);
});


const group = document.querySelector('.fa.fa-chevron-right').parentElement;
const idk = document.querySelectorAll('input[type="checkbox"]');
let visible = true;
group.addEventListener('click', function() {
	if(visible == false) {
		const folder = document.querySelector('#groups').removeAttribute('hidden');
		visible = true;
	} else {
		const folder = document.querySelector('#groups').setAttribute('hidden', "");
		visible = false;
	}
});

idk.forEach(function(box) {
    box.addEventListener('click', function(e) {
        const tr = e.target.parentElement.parentElement;
        if(e.target.checked) {
            if(tr.classList.contains('table-secondary')) {
                tr.classList.remove('table-secondary');
                tr.classList.add('read');
            }
            tr.classList.add('bg-info');
            tr.classList.add('text-white');
        } else if(e.target.checked == false) {
            if(tr.classList.contains('read')) {
                tr.classList.remove('read');
                tr.classList.add('table-secondary');
            }
            tr.classList.remove('bg-info');
            tr.classList.remove('text-white');
        }
        e.cancelBubble = true;
    });
});

// for marking as read
$('.fa.fa-envelope-o').click(function(event) {
    mail_ids = [];
    $('input[name="selectMail"]').each(function (index, value) {
        if ($(this)[0].checked) {
            $(this).parent().parent().removeClass('bg-info');
            $(this).parent().parent().removeClass('text-white');
            $(this).parent().parent().addClass('table-secondary')
            mail_ids.push($(this).parent().parent().data('id'));
            console.log(mail_ids);
        }
    })
});

// for making unread
$('.fa.fa-envelope-open-o').click(function(event) {
    mail_ids = [];
    $('input[name="selectMail"]').each(function (index, value) {
        if ($(this)[0].checked) {
            $(this).parent().parent().removeClass('bg-info');
            $(this).parent().parent().removeClass('text-white');
            $(this).parent().parent().addClass('table-secondary')
            mail_ids.push($(this).parent().parent().data('id'));
            console.log(mail_ids);
        }
    })
});

// for archiving
$('.fa.fa-archive').click(function(event) {
    mail_ids = [];
    $('input[name="selectMail"]').each(function (index, value) {
        if ($(this)[0].checked) {
            $(this).parent().parent().removeClass('bg-info');
            $(this).parent().parent().removeClass('text-white');
            $(this).parent().parent().addClass('table-secondary')
            mail_ids.push($(this).parent().parent().data('id'));
            console.log(mail_ids);
        }
    })
});

// for deleting
$('.fa.fa-trash').click(function(event) {
    mail_ids = [];
    $('input[name="selectMail"]').each(function (index, value) {
        if ($(this)[0].checked) {
            $(this).parent().parent().removeClass('bg-info');
            $(this).parent().parent().removeClass('text-white');
            $(this).parent().parent().addClass('table-secondary')
            mail_ids.push($(this).parent().parent().data('id'));
            console.log(mail_ids);
        }
    })
});


$('tr[data-href]').on('click', function() {
    window.location.href = $(this).data('href');
});