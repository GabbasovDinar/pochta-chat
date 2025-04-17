$(document).ready(function() {

    // API URLs
    const BACKEND_URL = window.APP_CONFIG.BASE_URL; // например, "http://localhost:8000"
    const API_BASE = "/api/v1";
    const BACKEND_API_URL = BACKEND_URL + API_BASE;

    // Для WS нужно убрать протокол из BACKEND_URL:
    const WS_URL = "ws://" + BACKEND_URL.replace(/^https?:\/\//, "") + "/websocket/connection";

    // WebSocket connection
    let socket = null;
    let currentChatId = null;
    let usersGlobal = []; // Глобальный массив для списка всех пользователей
    let currentUserId = null; // ID текущего пользователя
    let messages = []; // массив для хранения сообщений


    // Helper functions for cookies
    function getCookie(name) {
        const value = "; " + document.cookie;
        const parts = value.split("; " + name + "=");
        if (parts.length === 2) return parts.pop().split(";").shift();
        return null;
    }

    function setCookie(name, value, minutes) {
        let expires = "";
        if (minutes) {
            const date = new Date();
            date.setTime(date.getTime() + (minutes * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    // Для проверки соединения с backend
    async function checkConnection() {
        try {
            const response = await fetch(BACKEND_URL + "/ping");
            const data = await response.json();
            if (response.ok && data.message === "pong") {
                alert("Соединение успешно установлено");
            } else {
                alert("Соединение не установлено");
            }
        } catch (err) {
            alert("Ошибка соединения: " + err.message);
        }
    }

    async function getMe() {
        const token = getCookie("token");
        const response = await fetch(BACKEND_API_URL + "/users/me", {
            headers: { "Authorization": "Bearer " + token }
        });
        if (!response.ok) {
            const errData = await response.json();
            console.error(errData);
            alert("Ошибка получения текущего пользователя: " + errData.detail);
            throw new Error(errData.detail);
        }
        const user = await response.json();
        currentUserId = user.id;
        return user;
    }

    // Login, register user, log
    async function login(username, password) {
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(BACKEND_API_URL + "/users/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: formData.toString()
        });
        if (!response.ok) {
            const errData = await response.json();
            console.error(errData);
            alert("Ошибка логина проверьте правильность введенных данных. Ошибка: " + errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    async function register(name, email, password) {
        const response = await fetch(BACKEND_API_URL + "/users/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });
        if (!response.ok) {
            const errData = await response.json();
            console.error(errData);
            alert("Ошибка регистрации проверьте правильность введенных данных. Ошибка: " + errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    function logout() {
        setCookie("token", "", -1);
        location.reload();
    }

    // Event handlers for toggling forms
    function onClickRegisterLink(event) {
        event.preventDefault();
        $("#loginPage").hide();
        $("#registerPage").show();
    }

    function onClickLoginLink(event) {
        event.preventDefault();
        $("#registerPage").hide();
        $("#loginPage").show();
    }

    // обработчики форм
    async function onSubmitLoginForm(event) {
        event.preventDefault();
        const username = $("#loginUsername").val();
        const password = $("#loginPassword").val();
        try {
            const response = await login(username, password);
            setCookie("token", response.access_token, response.exp);
            await showMainPage();
        } catch (err) {
            alert("Ошибка логина: " + err.message);
        }
    }

    async function onSubmitRegisterForm(event) {
        event.preventDefault();
        const name = $("#registerUsername").val();
        const email = $("#registerEmail").val();
        const password = $("#registerPassword").val();
        try {
            const response = await register(name, email, password);
            alert("Регистрация успешна");
            $("#registerPage").hide();
            $("#loginPage").show();
        } catch (err) {
            alert("Ошибка регистрации: " + err.message);
        }
    }

    // WebSocket connection
    function connectWebSocket() {
        const token = getCookie("token");
        socket = new WebSocket(WS_URL + "?token=" + token);
        socket.onopen = function () {
            console.log("WebSocket соединение установлено");
        };
        socket.onmessage = function (event) {
            const data = JSON.parse(event.data);
            if (currentChatId && data.chat_id === currentChatId) {
                if (messages.find(m => m.id === data.message_id)) {
                    updateMessage(data.message_id, data);
                } else {
                    appendMessage(data);
                    // sendReadNotification(data.chat_id, data.id);
                }
            }
        };
        socket.onclose = function () {
            console.log("WebSocket соединение закрыто");
        };
        socket.onerror = function (error) {
            console.error("WebSocket ошибка: ", error);
        };
    }

    // отправка уведомления о прочтении сообщения
    function sendReadNotification(chatId, messageId) {
        const readNotification = {
            action: "read",
            chat_id: chatId,
            message_id: messageId
        };
        socket.send(JSON.stringify(readNotification));
    }

    // Join, leave chat
    async function joinChat(chatId) {
        const token = getCookie("token");
        const response = await fetch(BACKEND_API_URL + "/chats/join/" + chatId, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }
        });
        if (!response.ok) {
            const errData = await response.json();
            alert(errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    async function leaveChat(chatId) {
        const token = getCookie("token");
        const response = await fetch(BACKEND_API_URL + "/chats/leave/" + chatId, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            }
        });
        if (!response.ok) {
            const errData = await response.json();
            alert(errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    // Load chat history
    async function loadChatHistory(chatId) {
        const token = getCookie("token");
        const response = await fetch(BACKEND_API_URL + "/chats/history/" + chatId + "?limit=100&offset=0", {
            headers: { "Authorization": "Bearer " + token }
        });
        if (!response.ok) {
            const errData = await response.json();
            console.error(errData);
            alert("Ошибка загрузки истории чата. Ошибка: " + errData);
            throw new Error(errData);
        }
        const data = await response.json();
        if (data) {
            return data.result;
        }
        return [];
    }

    // Append message to chat window
    function appendMessage(message) {
        messages.push(message);
        // Находим автора сообщения в глобальном списке пользователей
        const user = usersGlobal.find(u => String(u.id) === String(message.user_id));
        const isCurrentUser = user && user.id === currentUserId;
        const alignmentClass = isCurrentUser ? "text-end" : "text-start";

        const statusText = isCurrentUser ? ` [${message.status}]` : "";

        const msgHtml = `<div class="${alignmentClass}" data-message-id="${message.id}">
            <strong>${user ? user.name : "Неизвестно"}:</strong> ${message.content}
            <small>(${new Date(message.timestamp).toLocaleTimeString()})${statusText}</small>
        </div>`;
        $("#chatWindow").append(msgHtml);
        $("#chatWindow").scrollTop($("#chatWindow")[0].scrollHeight);
    }

    // Обновление конкретного сообщения
    function updateMessage(messageId, message) {
        // находим сообщение в окне чата
        const msgHtml = $("#chatWindow").find(`[data-message-id="${messageId}"]`);
        if (msgHtml.length > 0) {
            // обновляем сообщение
            msgHtml.html(msgHtml.html() + `<small>(${new Date(message.timestamp).toLocaleTimeString()}) [${message.status}]</small>`);
        } else {
            appendMessage(message);
        }
    }

    // Функция открытия модального окна чата
    async function openChatModal(targetChatId, chatTitle) {
        // Очищаем окно чата
        $("#chatWindow").empty();
        // Загружаем историю чата
        const history = await loadChatHistory(targetChatId);
        history.forEach(function (message) {
            appendMessage({
                id: message.id,
                chat_id: message.chat_id,
                user_id: message.user_id,
                content: message.content,
                timestamp: message.created_at,
                status: message.status
            });
        });
        currentChatId = targetChatId;
        $("#chatModalLabel").text(chatTitle);
        $("#modalMessageInput").val("");
        const modalElement = document.getElementById("chatModal");
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }

    // Обработчик кнопки "Отправить" в модальном окне
    $("#modalSendMessageBtn").click(async function () {
        const message = $("#modalMessageInput").val();
        if (!message || !currentChatId) return;

        const data = { action: "create", chat_id: currentChatId, content: message };

        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(data));
            $("#modalMessageInput").val("");
        } else {
            connectWebSocket();
            alert("Ошибка отправки сообщения. Попробуйте отправить снова.");
        }
    });

    // Функция получения приватного чата (если не существует, то создается новый)
    async function preparePrivateChat(userId) {
        const token = getCookie("token");
        const response = await fetch(BACKEND_API_URL + "/chats", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                chat_type: "private",  // TODO: похорошему нужно делать отдельную ручку для приватных чатов
                user_ids: [userId]
            })
        });
        if (!response.ok) {
            const errData = await response.json();
            console.error(errData);
            alert("Ошибка получения приватного чата. Ошибка: " + errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    // Функция создания группового чата
    async function createGroupChat(chatName, selectedUserIds) {
        const token = getCookie("token");
        // Формируем объект запроса: название чата и список участников.
        const body = {
            chat_type: "group",
            name: chatName,
            user_ids: selectedUserIds
        };
        const response = await fetch(BACKEND_API_URL + "/chats", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(body)
        });
        if (!response.ok) {
            const errData = await response.json();
            alert("Ошибка создания группового чата. Ошибка: " + errData.detail);
            throw new Error(errData.detail);
        }
        return response.json();
    }

    // // Load all chats
    async function loadGroupChats() {
        const token = getCookie("token");
        try {
            const url = new URL(BACKEND_API_URL + "/chats/group");

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            });
            if (!response.ok) {
                const errData = await response.json();
                if (errData.detail === "Token has expired.") {
                    logout();
                }
                console.error(errData);
                return false;
            }
            const data = await response.json();
            let html = "";
            data.forEach(chat => {
                // Для чатов, если пользователь уже является участником,
                // показываем две кнопки: "Открыть" и "Выйти из чата".
                let buttonHtml = "";
                const isMember = chat.memberships.some(membership => membership.user_id === currentUserId);
                if (isMember) {
                    buttonHtml = `
                        <span>
                            <button class="btn btn-sm btn-primary openChat-btn"
                                data-chatid="${chat.id}"
                                data-chatname="${chat.name}"
                                data-is-member="true">
                                Открыть
                            </button>
                            <button class="btn btn-sm btn-danger leaveChat-btn"
                                data-chatid="${chat.id}">
                                Выйти из чата
                            </button>
                        </span>
                    `;
                } else {
                    // Если пользователь не состоит в чате – показываем кнопку "Вступить"
                    buttonHtml = `
                        <button class="btn btn-sm btn-primary joinChat-btn"
                            data-chatid="${chat.id}">
                            Вступить
                        </button>
                    `;
                }
                html += `
                    <div class="chat-item">
                        <span class="chat-name">${chat.name}</span>
                        ${buttonHtml}
                    </div>
                `;
            });
            $("#chatsList").html(html);

            $("#chatsList").off("click", ".joinChat-btn");
            $("#chatsList").off("click", ".leaveChat-btn");
            $("#chatsList").off("click", ".openChat-btn");

            // Обработчик для кнопок "Открыть"
            $("#chatsList").on("click", ".openChat-btn", function () {
                const chatId = $(this).data("chatid");
                const chatName = $(this).data("chatname");
                openChatModal(chatId, chatName);
            });

            // Обработчик для кнопок "Вступить"
            $("#chatsList").on("click", ".joinChat-btn", async function () {
                const chatId = $(this).data("chatid");
                await joinChat(chatId);
                // Обновляем список чатов после вступления в чат
                await loadGroupChats();
            });

            // Обработчик для кнопок "Выйти из чата"
            $("#chatsList").on("click", ".leaveChat-btn", async function () {
                const chatId = $(this).data("chatid");
                await leaveChat(chatId);
                // Обновляем список чатов после выхода из чата
                await loadGroupChats();
            });
        } catch (err) {
            alert("Ошибка загрузки всех чатов: " + err.message);
        }
    }

    // Load users
    async function loadUsers() {
        const token = getCookie("token");
        try {
            const response = await fetch(BACKEND_API_URL + "/users", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                }
            });
            if (!response.ok) {
                const errData = await response.json();
                if (errData.detail === "Token has expired.") {
                    logout();
                }
                throw new Error(errData.detail);
            }
            const data = await response.json();
            // Сохраняем глобально пользователей
            usersGlobal = data;
            // Отображаем список пользователей кроме себя
            let html = "";
            data.forEach(user => {
                if (user.id === currentUserId) {
                    $("#userName").text(user.name);
                } else {
                    html += `
                        <div class="user-item">
                            <span class="user-name">${user.name}</span>
                        <button class="btn btn-sm btn-primary write-btn" data-userid="${user.id}" data-username="${user.name}">
                            Написать
                        </button>
                        </div>
                    `;
                }
            });
            $("#usersList").html(html);
            $(".write-btn").click(async function () {
                const userId = $(this).data("userid");
                // получаем id чата и имя чата для указанного пользователя
                const chat = await preparePrivateChat(userId);
                if (chat) {
                    // открываем модальное окно для чата для указанного пользователя
                    openChatModal(chat.id, "Чат с " + chat.name);
                } else {
                    alert("Ошибка получения чата: " + err.message);
                }
            });
        } catch (err) {
            alert("Ошибка загрузки пользователей: " + err.message);
        }
    }

    // Функция открытия модального окна для создания группового чата
    async function openGroupChatModal() {
        $("#groupChatUsersList").empty();
        $("#groupChatName").val("");

        if (usersGlobal.length === 0) {
            // Если список еще не загружен, загрузим его через loadUsers (и сохраним в usersGlobal)
            await loadUsers();
        } else {
            renderUsersForGroupChat();
        }
        const modalElement = document.getElementById("groupChatModal");
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }

    // Функция для отображения списка пользователей с чекбоксами в модальном окне для группового чата
    function renderUsersForGroupChat() {
        let html = "";
        usersGlobal.forEach(user => {
            // Исключаем текущего пользователя из списка
            if (user.id !== currentUserId) {
                html += `
                    <div class="form-check">
                    <input class="form-check-input groupUserCheckbox" type="checkbox" value="${user.id}" id="userCheckbox_${user.id}">
                    <label class="form-check-label" for="userCheckbox_${user.id}">
                        ${user.name}
                    </label>
                    </div>
                `;
            }
        });
        $("#groupChatUsersList").html(html);

        // Обработчик кнопки "Создать чат"
        $("#createGroupChatConfirmBtn").click(async function () {
            const chatName = $("#groupChatName").val().trim();
            if (!chatName) {
                alert("Укажите название чата");
                return;
            }
            // Собираем выбранных пользователей (их ID)
            let selectedUserIds = [];
            $(".groupUserCheckbox:checked").each(function () {
                selectedUserIds.push($(this).val());
            });
            if (selectedUserIds.length === 0) {
                alert("Выберите хотя бы одного участника");
                return;
            }
            try {
                const newChat = await createGroupChat(chatName, selectedUserIds);
                // Закрываем модальное окно создания группового чата
                const modalElement = document.getElementById("groupChatModal");
                const modalInstance = bootstrap.Modal.getInstance(modalElement);
                modalInstance.hide();
                // Обновляем список чатов
                await loadGroupChats();
                // Открываем модальное окно для нового чата
                openChatModal(newChat.id, newChat.name);
            } catch (err) {
                alert("Ошибка создания группового чата: " + err.message);
            }
        });
    }

    // Show main page: скрываем формы, отображаем основное окно, запускаем WS и загружаем данные
    async function showMainPage() {
        $("#loginPage").hide();
        $("#registerPage").hide();
        $("#mainPage").show();
        await getMe();
        connectWebSocket();
        loadUsers();
        loadGroupChats();
    }

    // Initialize the application
    async function init() {
        $("#checkConnectionBtn").click(checkConnection);
        $("#logoutBtn").click(logout);
        $("#showRegisterLink").click(onClickRegisterLink);
        $("#showLoginLink").click(onClickLoginLink);
        $("#loginForm").submit(onSubmitLoginForm);
        $("#registerForm").submit(onSubmitRegisterForm);
        $("#createGroupChatBtn").click(openGroupChatModal);
        const token = getCookie("token");
        if (token) {
            await showMainPage();
        } else {
            $("#loginPage").show();
        }
    }

    init();

});
