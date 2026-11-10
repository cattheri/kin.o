// ===================================
//  РЕГИСТРАЦИЯ
// ===================================

const USERS_KEY = 'kin_o_users';

function getUsers() {
    const data = localStorage.getItem(USERS_KEY);
    return data ? JSON.parse(data) : [];
}

function saveUsers(users) {
    localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

function findUser(login) {
    return getUsers().find(u => u.login.toLowerCase() === login.toLowerCase());
}

document.getElementById('reg-btn').addEventListener('click', (e) => {
    e.preventDefault();

    const fio       = document.getElementById('reg-fio').value.trim();
    const email     = document.getElementById('reg-email').value.trim();
    const login     = document.getElementById('reg-login').value.trim();
    const password  = document.getElementById('reg-password').value;
    const password2 = document.getElementById('reg-password2').value;

    if (!fio || !email || !login || !password || !password2) {
        alert('Заполните все поля');
        return;
    }

    if (password.length < 4) {
        alert('Пароль должен быть не короче 4 символов');
        return;
    }

    if (password !== password2) {
        alert('Пароли не совпадают');
        return;
    }

    if (findUser(login)) {
        alert('Такой логин уже занят');
        return;
    }

    const users = getUsers();
    users.push({ fio, email, login, password });
    saveUsers(users);

    alert('Регистрация успешна!');
    window.location.href = 'auth.html';
});