function adicionarItem(produtoId) {
    fetch(`/pedido/carrinho/adicionar/${produtoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            // Atualizar a quantidade de itens no carrinho
            document.getElementById('sacola-count').textContent = data.quantidade_total;
            let sacolaIcone = document.getElementById('sacola-icon');
            sacolaIcone.className = 'bi-bag-fill fs-5 me-1';
            atualizarCarrinho()
        })
        .catch(error => {
            console.error('Erro ao adicionar item ao carrinho:', error);
        });
}


function tirarItem(produtoId) {
    fetch(`/pedido/carrinho/tirar/${produtoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            // Atualizar a quantidade de itens no carrinho
            document.getElementById('sacola-count').textContent = data.quantidade_total;
            let sacolaIcone = document.getElementById('sacola-icon');
            sacolaIcone.className = 'bi-bag-fill fs-5 me-1';

            if (data.quantidade_total - 1 === 0) {
                removerItem(produtoId); // Aciona removerItem se quantidade_total for zero
            }

            atualizarCarrinho()
        })
        .catch(error => {
            console.error('Erro ao adicionar item ao carrinho:', error);
        });
}


function removerItem(produtoId) {
    fetch(`/pedido/carrinho/remover/${produtoId}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            // Atualizar a quantidade de itens no carrinho
            document.getElementById('sacola-count').textContent = data.quantidade_total;
            let sacolaIcone = document.getElementById('sacola-icon');
            sacolaIcone.className = 'bi-bag-fill fs-5 me-1';
            atualizarCarrinho()
        })
        .catch(error => {
            console.error('Erro ao remover item ao carrinho:', error);
        });
}


document.addEventListener("DOMContentLoaded", () => {
    const sacolaCount = document.getElementById('sacola-count');
    const sacolaIcone = document.getElementById('sacola-icon');
    const carrinhoLink = document.querySelector(`a[href="{% url 'pedido:listar_carrinho'%}"]`);

    // Transforma o valor de innerText para inteiro
    const totalItensInt = parseInt(sacolaCount.innerText, 10);

    // Condicional para console.log
    if (totalItensInt > 0) {
        sacolaIcone.className = 'bi-bag-fill fs-5 me-1';

    } else {

        sacolaIcone.className = 'bi bi-bag fs-5 me-1';
    }
});


function atualizarCarrinho() {
    fetch('/pedido/carrinho/')
        .then(response => response.json())
        .then(data => {
            const tabelaItens = document.getElementById("tabela-itens");
            const totItems = document.getElementById("tot_items");
            const totAcumulado = document.getElementById("tot_acumulado");
            console.log(totItems)

            // Limpa a tabela antes de adicionar novos itens
            tabelaItens.innerHTML = "";

            // Preenche a tabela com os itens do carrinho
            const carrinho = data.carrinho;
            let totalItens = 0;

            for (const key in carrinho) {
                const item = carrinho[key];
                totalItens += item.quantidade;

                const row = `
                <tr class="text_menu text-sm">
                    <td>${item.nome}</td>
                    <td>
                        <a href="#" class="fs-3 pe-2" onclick="tirarItem(${item.id_prod})">
                                -
                        </a>
                        ${item.quantidade}
                        <a href="#" class="fs-3 ps-2" onclick="adicionarItem(${item.id_prod})">
                                +
                        </a>
                    </td>
                    <td>R$ ${item.preco.toFixed(2)}</td>
                    <td>R$ ${item.total.toFixed(2)}</td>
                    <td>
                        <a href="#" class="fs-3 pe-2" onclick="removerItem(${item.id_prod})">
                        <i class="bi bi-trash3-fill fs-5 text-danger"></i>
                        </a>
                    </td>
                </tr>
            `;
                tabelaItens.insertAdjacentHTML("beforeend", row);
            }

            // Atualiza os totais
            totItems.textContent = totalItens;
            totAcumulado.textContent = `R$ ${data.total_pedido.toFixed(2)}`;
        })
        .catch(error => {
            console.error("Erro ao buscar dados do carrinho:", error);
        });
}

// Chama a função para atualizar o carrinho ao carregar a página
document.addEventListener("DOMContentLoaded", atualizarCarrinho);
