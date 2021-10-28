import React, { useContext, useState } from "react";
import { Context } from "../store/appContext";
import "../../styles/home.scss";

export const Home = () => {
	const { store, actions } = useContext(Context);
	const [files, setFiles] = useState([]);

	const upload = event => {
		setFiles(event.target.files);
	};

	const save = async () => {
		const data = new FormData();
		data.append("file", files[0]);

		const response = await fetch(process.env.BACKEND_URL + "/api/upload-file", {
			method: "POST",
			body: data
		});
		console.log(response.status);
	};
	return (
		<div className="text-center mt-5">
			<h1>Subida de Ficheros</h1>
			<p>
				<input type="file" onChange={upload} />
				<input type="button" onClick={save} value="save" />
			</p>
			<div className="alert alert-info">{store.message || "Loading message from the backend..."}</div>
			<p>
				This boilerplate comes with lots of documentation:{" "}
				<a href="https://github.com/4GeeksAcademy/react-flask-hello/tree/95e0540bd1422249c3004f149825285118594325/docs">
					Read documentation
				</a>
			</p>
		</div>
	);
};

/* si colocamo multiple en el input podemos agregar varios */
