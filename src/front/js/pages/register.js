import React, { useState, useEffect, useContext } from "react";
import { Link } from "react-router-dom";

import "../../styles/demo.scss";

export const Register = () => {
	const [files, setFiles] = useState([]);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const upload = event => {
		setFiles(event.target.files);
	};

	const save = async () => {
		const data = new FormData();
		data.append("file", files[0]);
		data.append("email", "mm225@gmail.com");
		data.append("password", "1151");

		const response = await fetch(process.env.BACKEND_URL + "/api/register", {
			method: "POST",
			body: data
		});
		console.log(response.status);
	};

	return (
		<div className="container">
			<input type="text" placeholder="email" onChange={upload} />
			<input type="text" placeholder="password" onChange={upload} />
			<input type="file" onChange={upload} />
			<input type="button" onClick={save} value="save" />
			<br />
			<Link to="/">
				<button className="btn btn-primary">Back home</button>
			</Link>
		</div>
	);
};
