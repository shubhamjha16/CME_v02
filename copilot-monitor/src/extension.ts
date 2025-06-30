import * as vscode from 'vscode';
import axios from 'axios';

let lastPrompt = '';

export function activate(context: vscode.ExtensionContext) {
	console.log('✅ Copilot Monitor extension is now active!');

	vscode.workspace.onDidChangeTextDocument(async event => {
		const doc = event.document;

		// Only track supported languages
		if (!['python', 'typescript', 'javascript'].includes(doc.languageId)) return;

		const changes = event.contentChanges.map(c => c.text).join('').trim();
		if (!changes) return;

		// Heuristic: short = prompt, long = Copilot suggestion
		if (changes.length < 20) {
			lastPrompt = changes;
		}

		if (changes.length >= 20) {
			const suggestion = changes;

			try {
				const res = await axios.post('http://127.0.0.1:5000/score', {
					prompt: lastPrompt,
					suggestion,
					lang: doc.languageId,
					file_path: doc.fileName,
				});

				const score = res.data.score;
				vscode.window.showInformationMessage(`💡 Copilot Monitor Score: ${score}/10`);

			} catch (error: any) {
				if (axios.isAxiosError(error)) {
					console.error('❌ API Error:', error.response?.data || error.message);
					vscode.window.showErrorMessage(`Copilot Monitor: ${error.message}`);
				} else {
					console.error('❌ Unknown Error:', error);
					vscode.window.showErrorMessage('Copilot Monitor: Unknown error occurred.');
				}
			}
		}
	});
}

export function deactivate() { }