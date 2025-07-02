import * as vscode from 'vscode';
import axios from 'axios';
import axiosRetry from 'axios-retry';

// Apply retry logic to axios
axiosRetry(axios, {
	retries: 3, // number of retries
	retryDelay: (retryCount) => {
		console.log(`[CM] axios retry attempt: ${retryCount}`);
		return retryCount * 1000; // time interval between retries (ms)
	},
	retryCondition: (error) => {
		// retry on network errors or 5xx server errors
		return (
			axiosRetry.isNetworkError(error) ||
			axiosRetry.isRetryableError(error) // Handles 5xx errors
		);
	},
	onRetry: (retryCount, error, requestConfig) => {
		console.log(`[CM] Retrying request to ${requestConfig.url}, attempt ${retryCount}`, error.message);
	}
});

let lastPrompt = '';
const MAX_STORED_SUGGESTIONS = 20;
const scoredSuggestionsHistory: ScoredSuggestion[] = [];
let outputChannel: vscode.OutputChannel;

interface ScoredSuggestion {
	prompt: string;
	suggestion: string;
	score: number;
	lang: string;
	filePath: string;
	timestamp: Date;
}

// Helper function for logging to both console and output channel
function log(message: string, data?: any) {
	const fullMessage = data ? `${message} ${JSON.stringify(data, null, 2)}` : message;
	console.log(fullMessage);
	if (outputChannel) {
		outputChannel.appendLine(fullMessage);
	}
}

function logError(message: string, error?: any) {
	const fullMessage = error ? `${message} ${JSON.stringify(error, Object.getOwnPropertyNames(error), 2)}` : message;
	console.error(fullMessage);
	if (outputChannel) {
		outputChannel.appendLine(`ERROR: ${fullMessage}`);
	}
}


export function activate(context: vscode.ExtensionContext) {
	outputChannel = vscode.window.createOutputChannel("Copilot Monitor");
	context.subscriptions.push(outputChannel); // Add to subscriptions to dispose when extension deactivates
	log('✅ Copilot Monitor extension is now active!');

	// Command to view history (for potential future use with webview/output channel)
	// For now, it just logs to console for debugging this step
	context.subscriptions.push(vscode.commands.registerCommand('copilot-monitor.viewHistory', () => {
		log('[CM] Displaying suggestion history:');
		if (scoredSuggestionsHistory.length === 0) {
			log('[CM] No suggestions recorded yet.');
			vscode.window.showInformationMessage('Copilot Monitor: No suggestions recorded yet.');
			return;
		}
		scoredSuggestionsHistory.forEach((item, index) => {
			log(`[CM] ${index + 1}: Score ${item.score}/10 for lang ${item.lang} in ${item.filePath} (Prompt: "${item.prompt.substring(0,30)}...", Suggestion: "${item.suggestion.substring(0,50)}...")`);
		});
		// This could be expanded to show in a quick pick, output channel, or webview
		vscode.window.showInformationMessage(`Copilot Monitor: Logged ${scoredSuggestionsHistory.length} suggestions to console/output channel.`);
		outputChannel.show(true); // Optionally show the output channel
	}));


	vscode.workspace.onDidChangeTextDocument(async event => {
		log('[CM] onDidChangeTextDocument triggered');
		const doc = event.document;

		// Only track supported languages
		if (!['python', 'typescript', 'javascript'].includes(doc.languageId)) {
			log(`[CM] Document language ${doc.languageId} not supported, skipping.`);
			return;
		}

		const changes = event.contentChanges.map(c => c.text).join('').trim();
		if (!changes) {
			log('[CM] No changes detected, skipping.');
			return;
		}
		log(`[CM] Changes detected: "${changes}"`);

		// Heuristic: short = prompt, long = Copilot suggestion
		if (changes.length < 20) {
			lastPrompt = changes;
			log(`[CM] Identified as prompt. lastPrompt set to: "${lastPrompt}"`);
		}

		if (changes.length >= 20) {
			const suggestion = changes;
			log(`[CM] Identified as suggestion: "${suggestion}"`);
			log(`[CM] Current lastPrompt: "${lastPrompt}"`);

			const payload = {
				prompt: lastPrompt,
				suggestion,
				lang: doc.languageId,
				file_path: doc.fileName,
			};
			log('[CM] Sending to backend. Payload:', payload);

			try {
				const res = await axios.post('http://127.0.0.1:5000/score', payload);
				log('[CM] Backend response received:', res.data); // Log only res.data for brevity in output channel
				const score = res.data.score;
				vscode.window.showInformationMessage(`💡 Copilot Monitor Score: ${score}/10`);

				// Store the scored suggestion
				const entry: ScoredSuggestion = {
					...payload,
					score,
					timestamp: new Date()
				};
				scoredSuggestionsHistory.push(entry);
				if (scoredSuggestionsHistory.length > MAX_STORED_SUGGESTIONS) {
					scoredSuggestionsHistory.shift(); // Remove the oldest entry
				}
				log(`[CM] Stored suggestion. History size: ${scoredSuggestionsHistory.length}`);

			} catch (error: any) {
				logError('[CM] Error during API call:');
				if (axios.isAxiosError(error)) {
					logError('[CM] Axios Error details:', {
						message: error.message,
						code: error.code,
						status: error.response?.status,
						data: error.response?.data,
						// headers: error.response?.headers, // Potentially too verbose for output channel
						// config: error.config // Potentially too verbose
					});
					vscode.window.showErrorMessage(`Copilot Monitor: API Error - ${error.message}`);
				} else {
					logError('[CM] Non-Axios Error details:', error);
					vscode.window.showErrorMessage('Copilot Monitor: An unknown error occurred while scoring.');
				}
			}
		}
	});
}

export function deactivate() {
	log('[CM] Copilot Monitor extension deactivating.');
}