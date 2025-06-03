using System.Text;
using System.Windows;
using Polinom.ViewModel;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace Polinom
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private MainViewModel viewModel;
        public MainWindow()
        {
            InitializeComponent();
            viewModel = new MainViewModel();
            DataContext = viewModel;
            canvas.SizeChanged += Canvas_SizeChanged;
        }

        private void Canvas_SizeChanged(object sender, SizeChangedEventArgs e)
        {
            CreateLines();
            viewModel.Rebuild(canvas.ActualWidth, canvas.ActualHeight);
        }

        private void CreateLines()
        {
            var height = canvas.ActualHeight;
            var width = canvas.ActualWidth;
            linehor.X1 = 0;
            linehor.Y1 = height/2;
            linehor.X2 = width;
            linehor.Y2 = height/2;
            linevert.X1 = width/2;
            linevert.Y1 = height;
            linevert.X2 = width/2;
            linevert.Y2 = 0;
        }

        private void MouseDownClick(object sender, MouseButtonEventArgs e)
        {
            Point clickPoint = e.GetPosition(canvas);
            viewModel.ClickCommand.Execute(clickPoint);
        }
    }
}