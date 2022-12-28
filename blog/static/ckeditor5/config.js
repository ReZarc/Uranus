$(document).ready(function () {
    ClassicEditor
        .create(document.querySelector('#id_content'), {

            toolbar: {
                items: [
                    'heading',
                    '|',
                    'blockQuote',
                    'bold',
                    'fontColor',
                    'fontFamily',
                    'fontSize',
                    'italic',
                    'highlight',
                    'link',
                    'bulletedList',
                    'numberedList',
                    '|',
                    'outdent',
                    'indent',
                    '|',
                    'imageUpload',
                    'imageInsert',
                    'insertTable',
                    'mediaEmbed',
                    'undo',
                    'redo',
                    'CKFinder',
                    'code',
                    'codeBlock',
                    'fontBackgroundColor',
                    'findAndReplace',
                    'horizontalLine',
                    'htmlEmbed',
                    'todoList',
                    'superscript',
                    'subscript',
                    'sourceEditing'
                ]
            },
            language: 'zh-cn',
            image: {
                toolbar: [
                    'imageTextAlternative',
                    'imageStyle:inline',
                    'imageStyle:block',
                    'imageStyle:side'
                ]
            },
            // 上传图片url配置
            ckfinder: {
                uploadUrl: '/uploads/'
            },
            table: {
                contentToolbar: [
                    'tableColumn',
                    'tableRow',
                    'mergeTableCells'
                ]
            },
            licenseKey: '',

        })
        .then(editor => {
            window.editor = editor;




        })
        .catch(error => {
            console.error('Oops, something went wrong!');
            console.error('Please, report the following error on https://github.com/ckeditor/ckeditor5/issues with the build id and the error stack trace:');
            console.warn('Build id: l0rtbv6zc870-j0z9q43obeqd');
            console.error(error);
        });
})