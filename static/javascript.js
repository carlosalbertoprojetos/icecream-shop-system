$(document).ready(function () {

    // Função para obter o CSRF token do cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Verifica se este cookie começa com o nome que estamos procurando
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Obtém o token CSRF
    var csrftoken = getCookie('csrftoken');

    // Configura o AJAX para enviar automaticamente o token CSRF no cabeçalho
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Altera a quantidade de Potes no carrinho.
    $(document).on('click', '.sacola_plus, .sacola_minus', function () {
        // Obtem o Identificador do Pote
        // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
        var poteId = $(this).closest('.pote-item').data('poteid');

        // Use .siblings() para encontrar o elemento irmão do botão clicado
        var inputCountPote = $(this).siblings('input.countCartItem_' + poteId);

        // Atualiza a quantidade no frontend
        if ($(this).hasClass('sacola_plus')) {
            // Incrementa a quantidade quando o botão de adição é clicado
            inputCountPote.val(parseInt(inputCountPote.val()) + 1);
        } else if ($(this).hasClass('sacola_minus')) {
            // Decrementa a quantidade, com um valor mínimo de 0, quando o botão de subtração é clicado
            inputCountPote.val(Math.max(parseInt(inputCountPote.val()) - 1, 1));
        }

        var currentValue = parseInt(inputCountPote.val());

        // Exibe a quantidade atual no console
        console.log("Quantidade Atual:", currentValue);

        $.ajax({
            url: "/atualiza_quantidade_sacola/",
            type: "POST",
            data: {
                "poteId": poteId,
                "novaQuantidade": currentValue,
            },
            success: function (response) {
                console.log(response);
                // Adicione aqui qualquer manipulação adicional após o sucesso da requisição.
                var atualizaValor = $('#atualizaValor'); // Substitua 'spanQuantidade_' pelo identificador real que você está usando

                atualizaValor.text(response['novo_valor']);

                console.log(response['message'])

                $('#messageAlert').text(
                    response['message']).fadeIn(400).delay(2000).fadeOut(400);
            },
            error: function (error) {
                console.error("Erro:", error);
            }
        });
    });

    // Remover Item da Sacola
    $(document).on('click', '.remove-item', function () {
        // Obtem o Identificador do Pote
        // closest procra o ancestral mais próximo subindo na hierarquia do DOM a partir do elemento atual
        var poteId = $(this).closest('.pote-item').data('poteid');

        console.log("Identificador do Item:", poteId);

        // Armazene uma referência ao elemento <li> correspondente
        var poteItem = $(this).closest('.pote-item');

        // Obtenha o token CSRF do cookie
        var csrftoken = getCookie('csrftoken');

        // Envio Ajax com o token CSRF para view atualiza quantidade
        $.ajax({
            url: "/remove_item_sacola/",
            type: "POST",
            data: { "poteId": poteId },
            beforeSend: function (xhr) {
                // Inclua o token CSRF no cabeçalho da requisição
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (response) {
                console.log("Sucesso:", response);


                // No success
                poteItem.fadeOut(400, function () {
                    $(this).remove();
                });

                var atualizaValor = $('#atualizaValor');

                atualizaValor.text(response['novo_valor']);
                console.log(response['message'])
                $('#messageAlert').text(
                    response['message']).fadeIn(400).delay(2000).fadeOut(400);


            },
            error: function (error) {
                console.error("Erro:", error);
                // Adicione aqui qualquer manipulação adicional em caso de erro.
            }
        });
    });


    // Retorna endereço ao digitar cep e número
    $("#cep").on('keyup', function () {
        var cep = $(this).val().replace(/\D/g, '');
        console.log(cep);

        if (cep.length === 8) {

            // Fazer a chamada AJAX para buscar o endereço com base no CEP
            $.ajax({
                url: 'https://viacep.com.br/ws/' + cep + '/json/',
                method: 'GET',
                success: function (data) {

                    var numero_casa = $("#numero_casa").val();

                    // Criar o endereço formatado
                    var enderecoFormatado = 'Logradouro: ' + data.logradouro + ', ' +
                        'Bairro: ' + data.bairro + ', ' +
                        'Cidade: ' + data.localidade + ', ' +
                        'Estado: ' + data.uf + numero_casa;

                    // Preencher o campo de endereço
                    $("#id_endereco").val(enderecoFormatado);
                },
                error: function (error) {
                    console.log("Erro ao buscar CEP:", error);
                    alert("Erro ao buscar CEP. Verifique se o CEP é válido.");
                }
            });
        }
    });

    $("#numero_casa").on('blur', function () {
        var numero_casa = $(this).val().replace(/\D/g, '');
        var cep = $("#id_endereco").val();
        var enderecoFormatado = cep + ', ' +
            'Número: ' + numero_casa;
        $("#id_endereco").val(enderecoFormatado);
    });
});
