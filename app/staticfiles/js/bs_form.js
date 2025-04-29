var bsSpiner = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="false" ></span>'

function addSpinerInSubmitButton(button) {
    var currentText = button.innerHTML
    button.innerHTML = bsSpiner + 'Загрузка'
    return currentText
}
function removeSpinerFromButton(button, text) {
    button.innerHTML = text
}


function toggleForm(form, disable = true) {
    const elements = form.querySelectorAll("input, textarea, select, button");
    elements.forEach(el => el.disabled = disable);
}

// Отключить форму
function disableForm(form) {
    toggleForm(form, true);
}

// Включить форму
function enableForm(form) {
    toggleForm(form, false);
}
class SpinnerButton{
    // TODO
}
const formInstances = new WeakMap();

class BsJsonForm {
    constructor(elem) {
        this.elem = elem
        this.was_changed = false
        this.is_disabled = false
        this._btn_old_text = '' // вынести логику в другой класс
        this.object_id = undefined
        this._submitFunction = null
        this._init()
        this._add_events()
        this.setInstance(elem)

    }

    static getInstance(formElement) {
        if (!(formElement instanceof HTMLElement) || formElement.tagName !== 'FORM') {
            throw new Error('Argument must be a valid HTML form element');
        }
        const instance = formInstances.get(formElement);
        if (!instance) {
            throw new Error('No BsJsonForm instance found for this form element');
        }
        return instance;
    }

    setInstance(elem){
        var instance = formInstances.get(elem);
        if (instance){
            instance.clearEvents()
        }
        formInstances.set(elem, this)
    }

    _init() {
        this.clearFields()
        this.hideErrors()
    }

    _add_events() {
        this.elem.querySelectorAll('.form-control,.form-select').forEach(elem => {  // нет поддержки других типов элементов
            elem.addEventListener('input', () => this._removeIsInvalid(elem))
        })
    }

    set submitFunction(func){
        this._submitFunction = func
        this.elem.addEventListener('submit', this._submitFunction)
    }

    get submitButton() {
        return this.elem.querySelector('button[type=submit]')
    }

    // убрать клас is-invalid с элемента и также убрать с формы
    _removeIsInvalid(elem) {
        elem.classList.remove('is-invalid')
        this.elem.classList.remove('is-invalid')
        this.was_changed = true
    }

    clearEvents(){
        this.elem.removeEventListener('submit', this._submitFunction)
        this.elem.querySelectorAll('.form-control,.form-select').forEach(elem => {  // нет поддержки других типов элементов
            elem.removeEventListener('input', () => this._removeIsInvalid(elem))
        })
    }

    toDict(formData) {
        if (this.is_disabled) {
            throw new Error("Cant get data - form disabled");
        }
        var formData = new FormData(this.elem)
        var object_data = Object.fromEntries(formData.entries());
        if (this.object_id) {
            object_data['id'] = this.object_id
        }
        return object_data
    }

    disable() {
        this._btn_old_text = addSpinerInSubmitButton(this.submitButton)
        disableForm(this.elem)
        this.is_disabled = true
    }
    enable() {
        removeSpinerFromButton(this.submitButton, this._btn_old_text)
        enableForm(this.elem)
        this.is_disabled = false
    }

    clearFields() {
        this.elem.querySelectorAll('input,textarea').forEach(elem => {
            elem.value = ''
        })
        this.elem.querySelectorAll('select').forEach(select => {
            select.querySelectorAll('option').forEach(option => {
                if (option.dataset.default == 'true') {
                    option.selected = true
                }
            })
        })
    }

    hideErrors() {
        this.elem.classList.remove('is-invalid')
        this.elem.querySelectorAll('.is-invalid').forEach(elem => {
            elem.classList.remove('is-invalid')
        })
    }

    showErrors(data) {
        // non_field_errors
        for (var [key, value] of Object.entries(data)) {
            if (key == 'non_field_errors') {
                var errorTextBlock = this.elem.querySelector('.non-field-invalid-feedback')
                var inputElem = this.elem
            } else {
                var errorTextBlock = this.elem.querySelector(`[name="${key}"] + .invalid-feedback`)
                var inputElem = this.elem.querySelector(`[name="${key}"]`)
            }
            if (errorTextBlock) {
                errorTextBlock.innerHTML = value
                inputElem.classList.add('is-invalid')
            } else {
                console.info(`Error_block for key "${key}"" not found`)
            }

        }
    }

    feed(data) {
        this.object_id = data['id']
        for (var [key, value] of Object.entries(data)) {
            var elem = this.elem.querySelector(`*[name="${key}"]`)
            if (elem) {
                if (elem.nodeName == 'SELECT') {
                    var options = elem.querySelectorAll('option')
                    options.forEach(option => {
                        if (option.value == value) {
                            option.selected = true
                            return
                        }
                    })
                } else if (elem.nodeName == 'INPUT') {
                    elem.value = value
                }
            } else {
                console.warn('Elem not found', key)
            }
        }
    }
}