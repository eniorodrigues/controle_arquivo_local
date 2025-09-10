function abrirModalEdicao(id) {
    fetch(`/get/${id}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("registro_id").value = id;
            document.getElementById("cliente").value = data.cliente || "";
            document.getElementById("responsavel").value = data.responsavel || "";
            document.getElementById("al_2023").value = data.al_2023 || "";
            document.getElementById("status_rel_2024").value = data.status_rel_2024 || "";
            document.getElementById("tipo_al").value = data.tipo_al || "";
            document.getElementById("anexos_al_rel").value = data.anexos_al_rel || "";
            document.getElementById("status_trello").value = data.status_trello || "";
            document.getElementById("observacoes").value = data.observacoes || "";

            document.getElementById("modal").style.display = "block";
        });
}

function fecharModal() {
    document.getElementById("modal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-edicao");
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const id = document.getElementById("registro_id").value;
        const formData = new FormData(form);

        fetch(`/edit/${id}`, {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert("Registro atualizado com sucesso!");
                location.reload();
            } else {
                alert("Erro ao atualizar.");
            }
        });
    });
});
