   M S B A M L   `   `   `  ����B  >Polinom, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null5clr-namespace:Polinom.ViewModelPolinom.ViewModel  5   	       Polinom.MainWindow   5   	   W SPresentationCore, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=9.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089R NWindowsBase, Version=9.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     5   	   R NSystem.Xaml, Version=9.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     5   	   @d2http://schemas.microsoft.com/expression/blend/2008     5   	   Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     5   	   1localclr-namespace:Polinom.ViewModel     5   	     � Title$  
MainWindow��5   	   .��5      �  � RowDefinitions 5   
   �� 5      $��40 �6   �� 5       � ColumnDefinitions 5   
   �� 5      .+�5   
   � $��0��6   $��0��6    5      �� 5       5      �� 5      �� 5      .+�5      �� $��0��6   $��0��6"   $'��!Построить полином��62   ��6N   �� *ClickCreatePolynom+�� 5      $��0��6   $��1��6"   $��Очистить поле��62   ��6J   �� *
ClickClear+5!      �� 5%   
   -   5         ��Name$ canvas��5%      $��1��6!   $��0��6.   
�������$
}�True��5&   6   $	��500��5'      $	��800��6   .+�5(      �� -   5         ��Name$ linehor��5(      
���   �$��1��63   �� 5)      -   5        $ linevert��5)      
���   �$��1��64   �� 5*      ��6   �� *Points+��5+      �� 5,      .R�5-      �� 5.      ��50      �� 51       �� 
TargetType" ��6   .�52      ��  �� Property �@��Left �� Value 68   �� *X+�� 53       �@��Top 68   �� *Y+�� 54       � �� 69   �� *Radius+�� 55       � �� 6:   �� *Radius+56      ��58      �� 59      .R�5:      A� 
���  ��6"   5;      5=      � 5>      
���   �$��2��6C    � Points 6   �� *	LagPoints+6C   5?      5@      5A      