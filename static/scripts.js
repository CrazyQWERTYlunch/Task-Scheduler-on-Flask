// Функция для отображения/скрытия формы обновления списка задач
function toggleUpdateForm(todoId) {
    const updateForm = document.getElementById(`update-form-${todoId}`);
    updateForm.style.display = updateForm.style.display === 'none' ? 'block' : 'none';
}

// Делегирование событий для кнопок "Редактировать"
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('edit-button')) {
        const todoId = event.target.getAttribute('data-todo-id');
        toggleUpdateForm(todoId);
    }
});

// Показать форму для создания нового списка задач при нажатии на кнопку
const createTodoBtn = document.getElementById('create-todo-btn');
const createTodoForm = document.getElementById('create-todo-form');
createTodoBtn.addEventListener('click', function() {
    createTodoForm.style.display = 'block';
});

