using AndroidX.Core.Provider;

namespace STaTE_App;

public partial class MainPage : ContentPage
{

	public MainPage()
	{
		InitializeComponent();

        StuLoginPageLayout.IsVisible = false;
        ProfLoginPageLayout.IsVisible = false;
        LoginPageLayout.IsVisible = true;
    }

	private void OnStuClicked(object sender, EventArgs e)
	{
        LoginPageLayout.IsVisible = false;
        StuLoginPageLayout.IsVisible = true;
    }
    private void OnProfClicked(object sender, EventArgs e)
    {
        LoginPageLayout.IsVisible = false;
        ProfLoginPageLayout.IsVisible = true;
    }

    private void OnStuEnterClicked(object sender, EventArgs e)
    {
        StuLoginEditor.IsVisible = false;
        ProfLoginEditor.IsVisible = false;
        StuEnter.IsVisible = false;
        ProfEnter.IsVisible = false;

        StuLoginBtn.IsVisible = true;
        ProfLoginBtn.IsVisible = true;
    }
    private void OnProfEnterClicked(object sender, EventArgs e)
    {
        StuLoginEditor.IsVisible = false;
        ProfLoginEditor.IsVisible = false;
        StuEnter.IsVisible = false;
        ProfEnter.IsVisible = false;

        StuLoginBtn.IsVisible = true;
        ProfLoginBtn.IsVisible = true;
    }
    private void OnLoginOptionsReturnClicked(object sender, EventArgs e)
    {
        StuLoginPageLayout.IsVisible = false;
        ProfLoginPageLayout.IsVisible = false;
        LoginPageLayout.IsVisible = true;
    }

}

