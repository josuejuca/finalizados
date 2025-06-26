async function fetchCertidaoPDF() {
    // Definição das variáveis de parâmetros
    const P_Identificador = 1;
    const P_Argumento_Pesquisa = "09235025133"; // Substituir pelo CPF/CNPJ desejado
    const P_Tipo_Certidao = 1;
    const P_Finalidade_Certidao = 21;
    const P_Area_Solicitacao = 1;
    const P_TurnstileToken = '0.0cR3nhXyupDONVfp3SBa3PmnwtiPbLBdZJeei4KuU8PRZYxq58PzoVhVOKIfXrLfjzgOqiMIKyzjbO-_Pcum7n9osL41Uo0yHydJ8VQw88X4jRfHoU-3KheIinZPNbFCY48SilTulhOHXN38CP5rPv1xpZ0tl4rJOJI2sYMgt0qx-LxYyYdCH-pTJY96O9k-80GNQVaE6IMC23KifB_O6BLC9VuVubKWVFZFZ-NzL-S25S-FdFZi1J7h7zja7hJTyx4vEeQsajuti004IAV4oHLl5ztGywcJObOLuYwMfF76MZ9lQyRyb3LrfeQ-_Bkry_opCrZxOSPbTmU8HZRcEAuN-BK9HcnPvyOce7BY5EWkK0KCnezjP8A2kHiYZ0ohdasCiMSOkAIsrvrE-1QNtciSdm3hE_te7D3TUnV7bOuODW4XilFAkw684a7Y1-c1OKy97bUH_ue3fV-rKkePdEO4SXfs8dzLsz0svokTU3ZRG_sjLH3HIJbOBs_BMfy3kF6fdcL3xOZcZziFCy_db6anHa-xdYf2VDMRGuTOtm2q9aVJnPWhbzpeW9GndqPI93D9aeOxIS8gteNXTlyvLgk6nn88p-kofycW7dK_Wo189e52Ab4Os2CUHAaPRNwTjdVR71qTVuSCPbs6H1ptdV_kljwYYavlmDsgXGGk_Qi-3IKYWbR1Wq7deLhJGHYwxBHdhkRynHYI3tNwccPy7A2Zv5mxDsW67OPBksG7_tDanBCCZqhy2XKkPJZ7Ev-Xz_bFnratfM64NQlp0hrkbAEMk52wblNaSARn3pVgKAx0l6d4ISMHzIFd8sIranvkIYcF6H_Xd9poOve-C_CJ3SMvSsXoTknQHoyHWa1FqGIHvVdvdf3a9Pzt8GO1PdIo03e1ZcCIFDwQkTb3X_AapQ.Hrz9gVtohzv-OZI83J27cw.3f952eb0984c1f316aa4eb515d17af5c2225c4a452c49686b5ba1d8955fc1bce';
    const P_TurnstileResponseToken = "IkVoVOWGiJiqVebDum+4Op/vCJaASLIUfsnMyahc+P5ofssgVWZYOvTTk98XcwuG+PIIFuWkFzSmplA3JrHVZpWXNhxc58e8ChdqmBa+JFw7rbggFlTHVpkuOw+MqN/3BCVIPOF9uI1FjfeTFUkhsWgdRSZNGwlNfHgAXQohdBgo7JsIo7soDf3F+y3vKx5nVvWY//LLTMqcyFk5Ypmv2Pl7QGZQE00Hnwwiv3pQKNPkBYuSEznUcsocPnEzTE5/aMDEc5A6Y2VFVs/Z80dAYXLVHpW39DBGFzsXcatVypQqJg8wtZ3ExEXJoIrecWqdIh55OIu47o2yfytOJz+BxD9iCl4WOqdJeLXdWqCKmjLKbUqvFxcKjo38drmAqkXNIzk3daxcGp0Vk97eIrtbWvsvqqffL6Si4g0mm9vI3lPnxjz7Bog8ofu2xB5ZuyTCcmvyjsrwmpX2IxyyclnlOj1yRiKMWgKk4X8Lt3zO3PxIFNdGBT3xOq5Oe41Oa+DM4WCZseCe20iZdjH0DOngzAd3tngxtH1o9Y6NPYUKnxUkhgtbqx7WFi4hzdvBTnmPdm9iHqukAviTWLtG1EIHEQiSV66pdRtq6LyFCkxuk2LNHTH1as6FL3m7WzppB4z3wDKzg71nHYjrzWY2Y1fcUh/fccQ12DbBdeQByLQM3W4xEESkVDlud3f27UjDE65v3p6FRsalNVWKnoJ/GbqxM6JKUCSsbxT5uz0AviYToKlmGNenymQHzjB+NQV9LbjDZXYvoNg/wBMNNNd1aS9UwbO2/N2aDAI7XlVhfDP6dzQdjbu+3OAjUgAqw7hnngTGUwExEszxRo8wfB8mJrGXxDxDSJQQ1/fBPnQgfHc42yU17ADmDqwKhCwmBlkUAxJ9nY4vwCV4+wVAerAt1NjMlxHiKGRw0kv8toiDkXyLHgTodUbNJJombP38nUvEOhUCj5qvyqCD89cDuzlKtLRBReQn4AsNEaJT1C3SnfaXy2Ync0gi2AO1DLItHGrOvnkzHJXwmfEW0XiQlzNf5dXt/QuWL2LWgM+jVU56O8vhsg1PKp+nYdIQWWiQcpxvEIQaMVNqa8ds5mJLTjqGC/7kfvI+ozum/MfFcHqtAW7ocXHFHQWO8pKUvXyNvsGVqw17TIIGyJcAYg1EK4H0clnTbVEd694bJawjMam7O4W0m+XWrccjuKr0pqzOkWuYZ/UDGB3Xb/gQqaeW8Dxt/jutQNfehQSVno3I4xq1IhNGC5GHPpVoo2kzpTpycOtDj044TW6BrBeJBPRMD9bFFiPKEnBaaRf5EmKMZDBt8ODFujOiaQJbKy5MD/YXWq2elyJJ2b5d+WU9OIBbgUotAXUmo5hqOmYCW6X9Y1DM4aF9Izw=";

    const url = `https://ww1.receita.fazenda.df.gov.br/WPI/api/Report/token/CertidaoDoUsuario_PF_PJ/pdf?P_Identificador=${P_Identificador}&P_Argumento_Pesquisa=${P_Argumento_Pesquisa}&P_Tipo_Certidao=${P_Tipo_Certidao}&P_Finalidade_Certidao=${P_Finalidade_Certidao}&P_Area_Solicitacao=${P_Area_Solicitacao}&P_TurnstileToken=${P_TurnstileToken}&P_TurnstileResponseToken=${P_TurnstileResponseToken}`;

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/pdf',
                'User-Agent': 'Mozilla/5.0'
            }
        });

        if (!response.ok) throw new Error(`Erro ao buscar PDF: ${response.status}`);

        const blob = await response.blob();
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = "Certidao.pdf";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);

        console.log("Download concluído!");

    } catch (error) {
        console.error("Erro:", error);
    }
}

fetchCertidaoPDF();