import React, { useState } from "react";

export default function TheoryHub() {

  const [menu, setMenu] = useState("teori");

  // data indikator
  const indikator = [
    {
      nama: "Fenolftalein",
      ph: "8.3 - 10",
      asam: "Tidak berwarna",
      basa: "Pink"
    },

    {
      nama: "Metil Jingga",
      ph: "3.1 - 4.4",
      asam: "Merah",
      basa: "Kuning"
    },

    {
      nama: "Bromtimol Biru",
      ph: "6.0 - 7.6",
      asam: "Kuning",
      basa: "Biru"
    }
  ];

  return (

    <div
      style={{
        background: "#0f172a",
        color: "white",
        padding: "20px",
        borderRadius: "10px"
      }}
    >

      {/* JUDUL */}
      <h1>ChemIndicator Learning Hub</h1>

      <p>
        Website pembelajaran indikator asam basa
      </p>

      {/* MENU */}
      <div style={{ marginBottom: "20px" }}>

        <button onClick={() => setMenu("teori")}>
          Teori
        </button>

        <button onClick={() => setMenu("indikator")}>
          Indikator
        </button>

        <button onClick={() => setMenu("faq")}>
          FAQ
        </button>

      </div>

      {/* TEORI */}
      {menu === "teori" && (

        <div>

          <h2>Teori Asam Basa</h2>

          <h3>1. Arrhenius</h3>
          <p>
            Asam menghasilkan ion H+ dan basa menghasilkan ion OH- di air.
          </p>

          <h3>2. Bronsted Lowry</h3>
          <p>
            Asam memberi proton dan basa menerima proton.
          </p>

          <h3>3. Lewis</h3>
          <p>
            Asam menerima pasangan elektron dan basa memberi pasangan elektron.
          </p>

        </div>
      )}

      {/* INDIKATOR */}
      {menu === "indikator" && (

        <div>

          <h2>Tabel Indikator</h2>

          <table border="1" cellPadding="10">

            <thead>
              <tr>
                <th>Indikator</th>
                <th>Trayek pH</th>
                <th>Warna Asam</th>
                <th>Warna Basa</th>
              </tr>
            </thead>

            <tbody>

              {indikator.map((item, index) => (

                <tr key={index}>

                  <td>{item.nama}</td>
                  <td>{item.ph}</td>
                  <td>{item.asam}</td>
                  <td>{item.basa}</td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>
      )}

      {/* FAQ */}
      {menu === "faq" && (

        <div>

          <h2>FAQ</h2>

          <h3>Apa itu indikator?</h3>

          <p>
            Indikator adalah zat yang berubah warna sesuai pH larutan.
          </p>

          <h3>Kenapa indikator penting?</h3>

          <p>
            Karena membantu menentukan sifat asam atau basa suatu larutan.
          </p>

        </div>
      )}

    </div>
  );
}asa")
