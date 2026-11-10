
const USERS_KEY = 'kin_o_users';
const CURRENT_USER_KEY = 'kin_o_current_user';

function getUsers() {
    const data = localStorage.getItem(USERS_KEY);
    return data ? JSON.parse(data) : [];
}

function findUser(login) {
    return getUsers().find(u => u.login.toLowerCase() === login.toLowerCase());
}

document.getElementById('auth-btn').addEventListener('click', (e) => {
    e.preventDefault();

    const login = document.getElementById('login').value.trim();
    const password = document.getElementById('password').value;

    if (!login || !password) {
        alert('Введите логин и пароль');
        return;
    }

    const user = findUser(login);

    if (!user) {
        alert('Пользователь не найден');
        return;
    }

    if (user.password !== password) {
        alert('Неверный пароль');
        return;
    }

    localStorage.setItem(CURRENT_USER_KEY, JSON.stringify({
        fio: user.fio,
        email: user.email,
        login: user.login
    }));

    alert('Добро пожаловать!');
    window.location.href = '../index.html';
});