using System;
using System.Windows;
using System.Windows.Controls;

namespace CalculatorApp
{
    public partial class MainWindow : Window
    {
        private double _firstNumber;
        private double _secondNumber;
        private string _operation;
        private bool _isNewNumber;

        public MainWindow()
        {
            InitializeComponent();
            ResetCalculator();
        }

        private void ResetCalculator()
        {
            _firstNumber = 0;
            _secondNumber = 0;
            _operation = "";
            _isNewNumber = true;
            Display.Text = "0";
        }

        private void BtnNumber_Click(object sender, RoutedEventArgs e)
        {
            Button button = (Button)sender;
            string number = button.Content.ToString();

            if (Display.Text == "0" || _isNewNumber)
            {
                Display.Text = number;
                _isNewNumber = false;
            }
            else
            {
                Display.Text += number;
            }
        }

        private void BtnDecimal_Click(object sender, RoutedEventArgs e)
        {
            if (_isNewNumber)
            {
                Display.Text = "0,";
                _isNewNumber = false;
            }
            else if (!Display.Text.Contains(","))
            {
                Display.Text += ",";
            }
        }

        private void BtnOperation_Click(object sender, RoutedEventArgs e)
        {
            Button button = (Button)sender;
            _operation = button.Content.ToString();
            _firstNumber = double.Parse(Display.Text);
            _isNewNumber = true;
        }

        private void BtnEquals_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(_operation))
                return;

            _secondNumber = double.Parse(Display.Text);
            double result = 0;

            switch (_operation)
            {
                case "+":
                    result = _firstNumber + _secondNumber;
                    break;
                case "-":
                    result = _firstNumber - _secondNumber;
                    break;
                case "*":
                    result = _firstNumber * _secondNumber;
                    break;
                case "/":
                    if (_secondNumber != 0)
                        result = _firstNumber / _secondNumber;
                    else
                    {
                        MessageBox.Show("Нельзя делить на ноль!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
                        ResetCalculator();
                        return;
                    }
                    break;
            }

            Display.Text = result.ToString();
            _firstNumber = result;
            _isNewNumber = true;
            _operation = "";
        }

        private void BtnClear_Click(object sender, RoutedEventArgs e)
        {
            ResetCalculator();
        }

        private void BtnBackspace_Click(object sender, RoutedEventArgs e)
        {
            if (Display.Text.Length > 1)
            {
                Display.Text = Display.Text.Substring(0, Display.Text.Length - 1);
            }
            else
            {
                Display.Text = "0";
            }
        }

        private void BtnPercent_Click(object sender, RoutedEventArgs e)
        {
            double number = double.Parse(Display.Text);
            Display.Text = (number / 100).ToString();
            _isNewNumber = true;
        }

        private void BtnPlusMinus_Click(object sender, RoutedEventArgs e)
        {
            if (Display.Text == "0")
                return;

            if (Display.Text.StartsWith("-"))
            {
                Display.Text = Display.Text.Substring(1);
            }
            else
            {
                Display.Text = "-" + Display.Text;
            }
        }
    }
}