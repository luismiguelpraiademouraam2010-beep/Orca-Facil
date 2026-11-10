const statusApi = document.getElementById("api-status");
const botao = document.getElementById("check-status");

async function verificarSistema() {
    statusApi.textContent = "Verificando conexão...";
    try {
        const resposta = await fetch("http://127.0.0.1:5000/api/status");
        const dados = await resposta.json();
        if (!resposta.ok) throw new Error("Banco indisponível");
        statusApi.textContent = `API: ${dados.api} | Banco: ${dados.banco_de_dados}`;
    } catch (erro) {
        statusApi.textContent = "API indisponível. Inicie o Flask e confira o MySQL.";
    }
}

botao.addEventListener("click", verificarSistema);
verificarSistema();
