
# 🚀 EMAG OrderFlow: AWS Serverless E-Commerce Pipeline

Welcome to **EMAG OrderFlow** – a modern, serverless solution for automating e-commerce order processing using AWS Step Functions, Lambda, DynamoDB, SES, and EventBridge Pipes.

---

## 🌟 Features

- **Order Validation**: Checks customer and item validity
- **Inventory Reservation**: Reserves stock for valid orders
- **Shipping Cost Calculation**: Calculates transport price based on destination
- **Payment Processing**: Initiates payment and updates order status
- **Email Notifications**: Sends confirmation or failure emails to customers
- **Infrastructure as Code**: CloudFormation template for easy deployment

---

## 🗂️ Project Structure

| File                              | Purpose                                      |
|-----------------------------------|----------------------------------------------|
| `cosminEMAG_state_machine.asl.json` | AWS Step Functions state machine definition  |
| `pipe_template.json`                | CloudFormation template for EventBridge Pipe |
| `cosminEnrich.py`                   | DynamoDB stream record transformer           |
| `cosminTestLambda.py`               | Order validation logic                       |
| `cosminOrderReservation.py`         | Inventory reservation logic                  |
| `cosminCalculateTransportPrice.py`  | Shipping cost calculator                     |
| `cosminInitiatePayment.py`          | Payment initiation & failure notification    |
| `cosminUpdateOrderStatus.py`        | Updates order status in DynamoDB             |
| `cosminSentMail.py`                 | Confirmation email sender                    |
| `cosminSentFailMail.py`             | Failure email sender                         |

---

## ⚡ Quick Start

1. **Configure AWS Resources**
	- Deploy DynamoDB tables, Lambda functions, SES email identities
2. **Update Placeholders**
	- Replace all `<PLACEHOLDER>` values in Python and JSON files with your own
3. **Deploy Infrastructure**
	- Use `pipe_template.json` for EventBridge Pipe
	- Deploy state machine from `cosminEMAG_state_machine.asl.json`
4. **Install Requirements**
	- Python 3.8+, `boto3` (`pip install boto3`)

---

## 🔒 Security & Privacy

- All sensitive values (emails, ARNs, table names, account IDs) are placeholders
- No real credentials or personal data are present

---

## 📖 Usage

- Configure AWS resources and environment variables
- Deploy Lambda functions and state machine
- Trigger workflow via DynamoDB stream or EventBridge Pipe

---

## 📝 License

This project is provided as a template for educational and demonstration purposes. Please review and adapt for production use.

---

## 💡 Suggested GitHub Repository Name

**emag-orderflow-serverless**

---

Enjoy building your scalable e-commerce automation pipeline! ✨
